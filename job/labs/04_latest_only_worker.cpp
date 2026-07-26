// algorithm은 p99 index에 사용할 std::sort를 제공한다.
#include <algorithm>
// chrono는 frame timestamp, sleep, latency 단위를 제공한다.
#include <chrono>
// cmath는 nearest-rank p99 위치를 올림하는 std::ceil을 제공한다.
#include <cmath>
// condition_variable은 새 frame 또는 종료 상태까지 worker를 잠재운다.
#include <condition_variable>
// cstddef는 size와 index에 쓰는 std::size_t를 정의한다.
#include <cstddef>
// cstdint는 frame sequence의 고정 폭 uint64_t를 정의한다.
#include <cstdint>
// iostream은 처리 통계를 표준 출력에 표시한다.
#include <iostream>
// mutex는 producer와 worker가 공유하는 latest frame을 보호한다.
#include <mutex>
// optional은 frame이 아직 없는 상태와 하나 있는 상태를 명시적으로 표현한다.
#include <optional>
// thread는 producer와 inference worker를 동시에 실행한다.
#include <thread>
// utility는 by-value 인수를 storage로 옮기는 std::move를 제공한다.
#include <utility>
// vector는 처리된 frame age 표본을 저장한다.
#include <vector>

// ms는 긴 std::chrono::milliseconds 이름을 짧게 쓰는 type alias다.
using Milliseconds = std::chrono::milliseconds;
// Clock은 system time 변경의 영향을 받지 않는 monotonic clock이다.
using Clock = std::chrono::steady_clock;

// Frame은 생산 시각과 sequence를 함께 전달하는 최소 입력 record다.
struct Frame {
  // sequence는 생성 순서와 drop을 추적한다.
  std::uint64_t sequence;
  // produced_at은 frame이 sensor/producer에서 준비된 monotonic 시각이다.
  Clock::time_point produced_at;
};

// LatestOnlyQueue는 대기 frame을 최대 한 개만 보관한다.
class LatestOnlyQueue {
 public:  // producer와 worker가 사용할 최소 동기화 API만 공개한다.
  // by-value 인수는 caller가 복사 또는 move를 선택하고 함수 안에서는 안전하게 소유한다.
  // 반환값 False는 Stop 이후 입력이 거부되었음을 뜻한다.
  bool Push(Frame frame) {
    // lock_guard는 scope 동안 mutex를 잠그고 종료 때 자동 해제한다.
    {
      // queue state를 읽고 바꾸는 모든 작업을 같은 mutex로 보호한다.
      const std::lock_guard<std::mutex> lock(mutex_);
      // Stop 뒤 새 frame을 받으면 worker가 이미 끝났을 수 있으므로 저장하지 않는다.
      if (stopped_) {
        // producer가 lifecycle 오류를 telemetry로 처리할 수 있게 False를 반환한다.
        return false;
      }
      // 아직 worker가 가져가지 않은 frame이 있으면 이번 frame이 그것을 대체한다.
      if (latest_.has_value()) {
        // replaced_는 backlog 대신 폐기한 오래된 frame 수다.
        ++replaced_;
      }
      // frame은 이 함수가 소유한 by-value 객체이므로 storage로 안전하게 move한다.
      latest_ = std::move(frame);
    }
    // mutex를 해제한 뒤 worker 한 명을 깨워 lock 경쟁을 줄인다.
    available_.notify_one();
    // frame이 정상적으로 queue에 수용되었음을 producer에 알린다.
    return true;
  }

  // Take는 frame이 생기거나 Stop이 호출될 때까지 기다린다.
  std::optional<Frame> Take() {
    // unique_lock은 condition_variable wait 중 mutex를 자동 해제·재획득한다.
    std::unique_lock<std::mutex> lock(mutex_);
    // predicate는 spurious wakeup에도 실제 조건을 다시 검사한다.
    available_.wait(lock, [this] { return stopped_ || latest_.has_value(); });
    // 종료되었고 남은 frame도 없으면 worker loop를 끝낼 nullopt를 반환한다.
    if (stopped_ && !latest_.has_value()) {
      // nullopt는 유효 Frame이 없다는 명시적 값이다.
      return std::nullopt;
    }
    // optional 안의 최신 Frame 값을 지역 변수로 복사한다.
    const Frame frame = *latest_;
    // worker가 가져갔으므로 대기 slot을 빈 상태로 바꾼다.
    latest_.reset();
    // 가져온 frame을 optional value로 반환한다.
    return frame;
  }

  // Stop은 더 이상 frame이 오지 않으며 worker가 종료해야 함을 알린다.
  void Stop() {
    // stopped_ 변경도 Take predicate와 같은 mutex로 보호한다.
    {
      // scope 기반 lock으로 예외가 있어도 mutex를 해제한다.
      const std::lock_guard<std::mutex> lock(mutex_);
      // 종료 상태를 영구적으로 True로 바꾼다.
      stopped_ = true;
    }
    // wait 중인 모든 worker가 종료 조건을 확인하게 깨운다.
    available_.notify_all();
  }

  // Replaced는 producer가 교체한 frame 수를 읽는다.
  std::size_t Replaced() const {
    // const 함수에서도 통계를 안전하게 읽기 위해 mutable mutex를 잠근다.
    const std::lock_guard<std::mutex> lock(mutex_);
    // 보호된 replaced_ 현재 값을 복사해 반환한다.
    return replaced_;
  }

 private:  // 불변식은 모든 state 접근이 mutex_ 아래에서 일어난다는 것이다.
  // mutable은 const 통계 함수가 synchronization 목적으로 mutex를 잠그게 한다.
  mutable std::mutex mutex_;
  // condition_variable은 polling 없이 worker를 대기시킨다.
  std::condition_variable available_;
  // latest_는 최대 한 개의 처리 대기 frame을 보관한다.
  std::optional<Frame> latest_;
  // stopped_는 queue 수명 종료 조건이다.
  bool stopped_{false};
  // replaced_는 worker보다 producer가 빠를 때 버린 오래된 frame 수다.
  std::size_t replaced_{0};
};

// main은 producer와 worker를 만들고 처리 age 분포를 출력한다.
int main() {
  // 공유 latest-only queue를 stack에 생성한다.
  LatestOnlyQueue queue;
  // processed는 worker만 쓰고 main은 join 뒤 읽으므로 happens-before가 성립해 atomic이 필요 없다.
  std::size_t processed = 0;
  // frame age도 worker만 쓰고 main은 join 뒤 읽으므로 같은 thread-confinement 규칙을 따른다.
  std::vector<double> ages_ms;
  // worker thread는 queue가 종료되고 남은 frame이 없을 때까지 실행한다.
  std::thread worker([&queue, &processed, &ages_ms] {
    // 무한 loop의 종료는 Take가 nullopt를 반환할 때 명시적으로 처리한다.
    while (true) {
      // 새 frame 또는 종료 상태까지 block한다.
      const std::optional<Frame> frame = queue.Take();
      // nullopt는 Stop 이후 처리할 frame이 없다는 뜻이다.
      if (!frame.has_value()) {
        // worker loop를 종료한다.
        break;
      }
      // 5 ms sleep은 target runtime의 추론 시간을 단순 simulation한다.
      std::this_thread::sleep_for(Milliseconds(5));
      // 처리 완료 시각을 monotonic clock에서 읽는다.
      const Clock::time_point finished_at = Clock::now();
      // 생산부터 처리 완료까지 microseconds 정수로 계산한다.
      const auto age_us =
          std::chrono::duration_cast<std::chrono::microseconds>(
              finished_at - frame->produced_at);
      // microseconds를 1000으로 나누어 소수 ms 표본으로 저장한다.
      ages_ms.push_back(static_cast<double>(age_us.count()) / 1000.0);
      // 단일 writer thread 안의 일반 정수 증가이므로 data race가 없다.
      ++processed;
    }
  });
  // producer thread는 2 ms마다 총 100개 frame을 만든다.
  std::thread producer([&queue] {
    // sequence 0부터 99까지 반복한다.
    for (std::uint64_t sequence = 0; sequence < 100; ++sequence) {
      // 현재 monotonic 시각을 frame 생산 시각으로 기록해 queue age를 잰다.
      const bool accepted = queue.Push(Frame{sequence, Clock::now()});
      // 이 예제에서는 Stop 전 producer만 Push하므로 거부는 lifecycle bug다.
      if (!accepted) {
        // 오류를 표준 오류에 남기고 더 이상 frame을 만들지 않는다.
        std::cerr << "producer attempted to push after queue stop\n";
        // producer loop를 종료한다.
        break;
      }
      // sensor가 2 ms period로 입력을 만드는 상황을 simulation한다.
      std::this_thread::sleep_for(Milliseconds(2));
    }
    // 모든 frame을 생산했으므로 queue와 worker에 종료를 알린다.
    queue.Stop();
  });
  // main은 producer가 모든 frame을 넣고 Stop할 때까지 기다린다.
  producer.join();
  // main은 worker가 남은 최신 frame까지 처리하고 끝날 때까지 기다린다.
  worker.join();
  // p99를 계산하려면 처리 age를 오름차순 정렬한다.
  std::sort(ages_ms.begin(), ages_ms.end());
  // 표본이 없을 때 index underflow를 피하기 위해 기본 p99를 0으로 둔다.
  double p99_ms = 0.0;
  // 정상 실습에서는 최소 한 frame이 처리되어야 한다.
  if (!ages_ms.empty()) {
    // nearest-rank는 ceil(p*N)-1이며 표본 수가 작아도 "99% 이하" 의미가 분명하다.
    const double one_based_rank =
        std::ceil(0.99 * static_cast<double>(ages_ms.size()));
    // one-based rank를 0-based index로 바꾸고 마지막 원소를 넘지 않게 제한한다.
    const std::size_t index = std::min(
        ages_ms.size() - 1,
        static_cast<std::size_t>(one_based_rank - 1.0));
    // 정렬된 해당 위치의 age를 p99로 선택한다.
    p99_ms = ages_ms[index];
  }
  // 실제 처리한 수를 출력한다.
  std::cout << "processed=" << processed << '\n';
  // worker가 가져가기 전에 최신 frame으로 교체된 수를 출력한다.
  std::cout << "replaced=" << queue.Replaced() << '\n';
  // 오래된 FIFO backlog를 쌓지 않은 상태의 p99 frame age를 출력한다.
  std::cout << "p99_frame_age_ms=" << p99_ms << '\n';
  // 정상 process 종료 코드 0을 반환한다.
  return 0;
}
