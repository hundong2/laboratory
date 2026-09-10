# 07. HAL·무선칩·RTOS

## 1. HAL Driver가 왜 필요한가

**HAL (Hardware Abstraction Layer, 하드웨어 추상화 계층)**은 application/protocol stack이 MCU(Microcontroller Unit, 마이크로컨트롤러) register와 board pin에 직접 의존하지 않게 한다. chip driver와 board support를 분리하면 SX1262를 다른 MCU로 옮기거나 mock device로 test하기 쉽다.

권장 층:

```text
application / radio service
 -> device driver state machine
 -> chip command/register layer
 -> HAL: SPI, GPIO, interrupt, timer
 -> BSP: board pin, TCXO, RF switch, power rail
 -> MCU peripheral registers
```

**BSP (Board Support Package, 보드 지원 패키지)**는 특정 PCB wiring과 clock/power 구성을 담는다. HAL API 안에 board pin number를 hard-code하지 않는다.

## 2. SPI Read/Write

**SPI (Serial Peripheral Interface, 직렬 주변장치 인터페이스)**는 SCLK(clock), MOSI(master out/slave in), MISO(master in/slave out), CS/NSS(chip select)로 synchronous full-duplex 전송한다.

확인 항목:

- CPOL(Clock Polarity)과 CPHA(Clock Phase), 즉 SPI mode
- maximum clock와 sleep/wake 때 낮아지는 제한
- MSB/LSB first, byte order
- CS setup/hold와 transaction 사이 timing
- DMA(Direct Memory Access) 완료와 cache coherency
- 여러 task의 bus mutex, ISR에서 SPI 사용 금지 여부

SX1276은 address MSB로 read/write를 구분하는 register transaction을 사용하고 FIFO burst가 가능하다. SX1262는 opcode, parameter, status/dummy byte를 포함한 command transaction이며 `BUSY` low를 확인해야 한다. 두 칩에 같은 register driver를 재사용할 수 없다.

안전한 HAL contract 예:

```c
typedef enum {
    RADIO_OK,
    RADIO_TIMEOUT,
    RADIO_BUS_ERROR,
    RADIO_INVALID_STATE
} radio_status_t;

radio_status_t radio_spi_transfer(
    const uint8_t *tx, uint8_t *rx, size_t length, uint32_t timeout_us);
```

timeout, partial transfer, chip select cleanup을 명시하고 error가 나도 bus lock이 풀리게 한다.

## 3. reset GPIO

**GPIO reset**은 chip을 known state로 되돌리는 hardware control이다. active-low인지, open-drain/floating이 필요한지, pulse width와 release 후 wait time을 데이터시트대로 구현한다.

reset sequence:

1. competing task와 IRQ mask/disable
2. SPI transaction 중단 및 CS inactive
3. reset pin assert, minimum duration 대기
4. reset release 및 chip-ready/BUSY wait
5. version/status sanity check
6. calibration, regulator, TCXO, RF switch 재설정
7. IRQ clear/mapping, packet type, frequency 재설정
8. state publish 후 task 재개

reset은 register configuration을 지우므로 단순 GPIO pulse가 아니다. repeated reset loop를 막기 위해 reset reason과 count를 non-volatile event log에 남긴다.

## 4. DIO interrupt mapping과 IRQ

**DIO (Digital Input/Output, 디지털 입출력)**는 radio event를 MCU pin으로 알린다. **IRQ (Interrupt Request, 인터럽트 요청)**는 peripheral이 CPU에 즉시 처리를 요청하는 signal이며, MCU는 ISR을 실행한다.

### SX1276

`RegDioMapping1/2`가 DIO0~DIO5에 RxDone, TxDone, RxTimeout, FhssChangeChannel, CadDone 등을 mode별 mapping한다. 동일 pin 의미가 LoRa/FSK와 state에 따라 바뀌므로 mapping change와 operation start를 atomic하게 관리한다.

일반 LoRa packet mode 예:

- DIO0 = RxDone 또는 TxDone
- DIO1 = RxTimeout
- DIO3 = ValidHeader/CadDone 등
- `RegIrqFlagsMask`는 event 발생 자체가 아니라 IRQ flag 사용을 mask
- 처리 후 `RegIrqFlags`에 1을 써 해당 flag clear

### SX1262

`SetDioIrqParams(irqMask, dio1Mask, dio2Mask, dio3Mask)` command로 global IRQ와 각 DIO route를 설정한다. DIO1을 consolidated IRQ로 주로 쓰고, DIO2는 external RF switch control, DIO3는 TCXO control로 전용할 수 있다. module schematic을 보지 않고 DIO2/3를 IRQ로 쓰면 hardware control과 충돌할 수 있다.

### ISR 원칙

```text
GPIO edge ISR:
  capture timestamp
  disable/debounce if needed
  notify high-priority radio worker
  return

radio worker task:
  wait BUSY if applicable
  read IRQ status
  clear handled flags
  read/write FIFO and status
  advance state machine
  re-enable interrupt
```

ISR에서 logging, dynamic allocation, long SPI polling, blocking mutex를 피한다. RTOS의 `FromISR` API처럼 ISR-safe API만 사용하고, higher-priority task가 깨면 context switch 요청을 정확히 전달한다.

### race condition

- IRQ edge 뒤 status read 전 새 event가 합쳐짐
- clear와 read 사이 event loss
- TxDone과 timeout timer가 동시에 발생
- reset 중 stale IRQ
- DIO pin stuck high로 interrupt storm

driver state, hardware IRQ bitmap, software event queue를 함께 검사하고 unexpected event를 버리지 말고 계수한다.

## 5. radio driver 상태기계

```text
UNINIT -> RESETTING -> STANDBY -> CONFIGURED
                       |  ^       |      |
                       v  |       v      v
                      SLEEP      RX <-> TX
                                   \-> CAD
ANY -> ERROR_RECOVERY -> RESETTING
```

각 transition에는 allowed source state, command, timeout, expected IRQ, rollback을 둔다. `bool busy` 하나로 표현하면 sleep wake, calibration, RxDutyCycle 같은 복합 상태에서 race가 생긴다.

## 6. RTOS

**RTOS (Real-Time Operating System, 실시간 운영체제)**는 결과의 논리적 정확성뿐 아니라 deadline 내 완료를 관리하는 OS다. 빠른 OS가 아니라 worst-case latency를 분석할 수 있어야 한다.

핵심 개념:

- **task/thread**와 priority
- preemptive/fixed-priority scheduling
- ISR latency와 context switch
- semaphore, mutex, queue, event flag
- software timer와 tick/tickless idle
- WCET(Worst-Case Execution Time, 최악 실행시간)
- priority inversion과 priority inheritance
- deterministic memory allocation

### Rate Monotonic 직관

period가 짧은 주기 task에 높은 priority를 주는 fixed-priority 방식이다. utilization만 통과했다고 deadline이 보장되는 것은 아니며 blocking, ISR, release jitter를 response-time analysis에 넣는다.

## 7. FreeRTOS

**FreeRTOS (Free Real-Time Operating System)**는 작은 microcontroller용 open-source real-time kernel이다. task, queue, semaphore/mutex, direct-to-task notification, software timer, stream/message buffer를 제공한다.

권장 pattern:

- ISR → direct task notification → driver task
- ownership transfer가 필요한 message → queue
- 단일 event count → counting semaphore 또는 notification
- shared SPI bus → mutex + priority inheritance
- high-rate byte stream → stream buffer/DMA ring

`xQueueSendFromISR` 등 `FromISR` suffix API만 ISR에서 사용한다. `configMAX_SYSCALL_INTERRUPT_PRIORITY`보다 높은 hardware interrupt priority에서는 kernel API를 부르면 안 되는 port가 많다.

동적 heap scheme은 mission policy에 맞게 선택한다. flight-critical path는 startup 때 정적으로 할당하고 runtime allocation failure를 설계상 제거하는 편이 검증하기 쉽다.

## 8. VxWorks

**VxWorks**는 Wind River의 commercial RTOS로 aerospace·defense·industrial safety-critical system에 사용된다. preemptive real-time scheduling, process/kernel partition, network stack, virtualization, safety/security certification artifact와 long-term support가 강점이다.

VxWorks 653 계열은 ARINC 653(Avionics Application Software Standard Interface) 기반 time/space partitioning을 강조한다. 복수 criticality application을 partition으로 격리할 때 유리하지만 schedule table과 inter-partition communication 설계가 복잡하다.

선택 기준은 kernel benchmark보다 다음이다.

- DO-178C/IEC 61508 등 목표 인증과 evidence
- BSP/processor/radiation-tolerant board 지원
- network/crypto stack와 export/control 조건
- toolchain qualification, trace, coverage
- long-term patch와 vendor support
- license와 per-device cost

## 9. Mbed OS

**Mbed OS**는 Arm Cortex-M IoT device를 위한 open-source platform OS로 RTOS, HAL, driver, connectivity, storage, security를 통합했다. 빠른 prototype과 board portability를 위해 탄생했다.

그러나 Arm은 Mbed Platform을 2026년 7월 sunset했고 Mbed OS를 더 이상 적극 유지·지원하지 않는다. source는 Apache-2.0으로 남고 community fork인 Mbed CE가 있으나, 신규 장기 위성 임무는 다음을 평가해야 한다.

- vulnerability patch 책임과 maintenance fork
- compiler/toolchain와 board support 수명
- LwM2M/LoRaWAN/TLS dependency version
- qualification evidence 재생성 비용
- FreeRTOS/Zephyr/commercial RTOS migration

기존 Mbed code는 HAL contract와 application logic을 먼저 분리해 단계적으로 이식한다. EOL은 즉시 작동 중단을 뜻하지 않지만 공급망 risk가 조직으로 이전된다는 뜻이다.

## 10. RTOS 선택 matrix

| 기준 | FreeRTOS | VxWorks | Mbed OS |
|---|---|---|---|
| 성격 | kernel 중심 open source | commercial integrated RTOS | IoT platform OS, Arm 지원 종료 |
| footprint | 작음 | 구성에 따라 큼 | connectivity 포함 비교적 큼 |
| 인증 | 별도 commercial offerings/evidence 확인 | safety portfolio 강점 | 신규 인증 유지 위험 |
| 생태계 | MCU 매우 넓음 | mission/safety vendor support | 기존 Cortex-M 자산 |
| 적합 | 비용·제어 중심 embedded | 고신뢰·인증·지원 중심 | legacy 유지/교육, 신규는 신중 |

## 11. 시험 전략

- fake SPI/GPIO로 state machine unit test
- logic analyzer로 CS, clock, BUSY, DIO timing 확인
- IRQ storm, missing IRQ, duplicate IRQ, stuck BUSY fault injection
- reset at every state와 power-cycle brownout test
- long-run Tx/Rx cycle에서 buffer·stack watermark
- concurrent SPI device arbitration과 priority inversion test
- hardware-in-the-loop Doppler, attenuation, packet loss
- radiation upset 가정으로 register bit flip과 memory ECC event 처리

[← 이전](06_iot_protocols.md) · [메인](../README.md) · [다음: 보안·품질 →](08_security_quality.md)
