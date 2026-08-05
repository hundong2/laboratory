# Hard Intersection Multimodal Sample 분석과 실습

작성일: 2026-08-06

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [데이터 품질과 주의점](#데이터-품질과-주의점)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 사용자 제공 페이지: [Voxel51/hard-intersection-multimodal-sample](https://huggingface.co/datasets/Voxel51/hard-intersection-multimodal-sample)
- source dataset: [dynamic-maps/hard-intersection-multimodal-sample](https://huggingface.co/datasets/dynamic-maps/hard-intersection-multimodal-sample)
- Voxel51 revision: `c9be8ed61671e518c9b57c90b5bc2b8c4b8dd3b6`
- 최근 수정: 2026-08-04 17:30:03 UTC
- 접근일: 2026-08-06
- 원문 언어: 영어
- license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 접근 상태: public, non-gated, enabled
- 확인 범위: dataset card, Hugging Face dataset API, file tree, FiftyOne metadata, `samples.json`, `frames.json`

제공 URL은 `dynamic-maps` 페이지로 redirect되는 주소가 아니라, 원본 자료를 FiftyOne grouped dataset으로 재구성한 별도의 Voxel51 repository입니다. 한국어로 재구성한 dataset card는 [`translation.ko.md`](translation.ko.md)에서 볼 수 있습니다.

## 한눈에 보기

이 dataset은 일본 도쿄 다카나와다이의 사고 위험이 높은 비정형 6거리 교차로를 네 번 주행하며 얻은 자료를, 다음과 같은 **4개 group**으로 묶은 소규모 multimodal sample입니다.

```text
episode group × 4
  ├─ Camera_0 video  ─ detections + HD map + trajectory
  ├─ Camera_1 video  ─ detections + HD map
  ├─ Camera_2 video  ─ detections + HD map
  ├─ Camera_3 video  ─ detections + HD map
  ├─ Camera_4 video  ─ detections + HD map
  ├─ Camera_5 video  ─ label 없음, top-view
  └─ point_cloud     ─ FO3D scene + PCD
```

총 28 sample은 24개 MP4와 4개 3D scene으로 구성됩니다. repository 전체 크기는 약 1.66GB(1.55GiB)이며, 각 group은 동일 episode의 camera·point cloud slice를 공유 group ID로 연결합니다.

## 기초 개념

### Grouped multimodal dataset

일반 image dataset에서는 sample 하나가 image 하나입니다. 이 자료에서는 주행 episode 하나가 여러 media slice를 가집니다. 학습·평가 split을 만들 때 slice를 무작위로 나누면 같은 장면의 다른 camera가 train과 test에 동시에 들어가는 leakage가 발생하므로 반드시 `episode_id` 또는 group 단위로 분리해야 합니다.

### Camera와 LiDAR

camera는 색과 texture를 제공하지만 깊이를 직접 측정하지 않습니다. LiDAR는 3차원 점을 측정하지만 이 sample의 PCD는 순간별 scan sequence가 아니라 여러 run을 합친 aggregated scene입니다. 따라서 camera frame과 “동시 LiDAR frame”을 일대일로 맞추는 연구에는 적합하지 않습니다.

### HD map projection

Lanelet2 map의 3D polyline을 camera intrinsics·extrinsics로 2D image에 투영해 `hd_map` label을 만듭니다. source 좌표계를 EPSG:6677로 맞추고 world-to-camera transform과 pinhole projection을 적용해야 합니다.

### FiftyOne native format

`metadata.json`, `samples.json`, `frames.json`이 dataset schema와 sample·frame label을 저장합니다. media file은 `data/`에 있고 `.fo3d`는 PCD asset을 참조합니다. `fo.Dataset.from_dir(..., dataset_type=fo.types.FiftyOneDataset)`로 불러올 수 있습니다.

## 핵심 요약

| 항목 | 확인 결과 |
|---|---|
| group | 4 driving episodes |
| sample | 28개: video 24 + 3D 4 |
| slice | Camera_0~5 + point_cloud |
| video | H.264/avc1, 2048×2464 portrait, episode별 약 1.54~2.34 FPS |
| label frame document | 560개: Camera_0~4의 source frame 112개씩 |
| `ground_truth` | 270 frame, 6,854 detections, 현재 sample에서 26 class 관측 |
| `hd_map` | 560 frame 전부 |
| `trajectory` | Camera_0의 112 frame |
| point cloud | episode별 PCD 4개, trajectory 30m 이내 subset |
| CRS | EPSG:6677, Japan Plane Rectangular CS IX |
| privacy | face mosaic·plate masking을 적용했으나 완전성 미보장 |

## 상세 정리

### 1. Dataset 목적

다카나와다이는 언덕 정상의 sensor blind spot, 급격한 curve를 포함한 6거리 구조, 좁은 도로의 centerline 침범, 복잡한 traffic signal과 occlusion이 겹치는 장소입니다. 이 sample은 대규모 범용 학습 corpus가 아니라 multi-camera perception, map projection, localization, point-cloud visualization과 safety edge-case pipeline을 시험하기 위한 작은 분석 단위입니다.

### 2. Episode와 media

| Episode | source frame 수 | encoded metadata frame 수 | FPS | duration |
|---|---:|---:|---:|---:|
| `26047_Record004_260217` | 28 | 29 | 2.037 | 14.24s |
| `26047_Record050_260217` | 26 | 27 | 2.052 | 13.16s |
| `26047a_Record004_260217` | 30 | 31 | 1.538 | 20.16s |
| `26047a_Record084_260217` | 28 | 29 | 2.339 | 12.40s |

Dataset card의 source frame 수와 MP4 container metadata의 frame 수가 episode마다 1씩 다릅니다. `frames.json`은 source 기준 112 frame에 Camera_0~4를 곱한 560 record입니다. video decode 결과와 label frame number를 결합할 때 이 off-by-one 가능성을 명시적으로 검사해야 합니다.

### 3. File 구성과 저장 용량

재귀 tree API에서 확인한 39개 file의 크기 합계는 1,659,090,565 bytes입니다. Dataset metadata API의 `usedStorage`는 1,659,041,863 bytes로 48,702 bytes 작으므로, 용량을 자동 검증할 때는 사용한 API endpoint와 revision을 함께 기록해야 합니다.

- 24 × MP4: 4 episode × 6 camera
- 4 × PCD: 약 160MB 두 개, 517MB·522MB 두 개
- 4 × FO3D: PCD를 참조하는 작은 scene descriptor
- `metadata.json`: FiftyOne dataset schema
- `samples.json`: 28 sample과 group membership
- `frames.json`: frame label 560개, 약 18.9MB
- `fiftyone.yml`, `README.md`, preview GIF, Git attributes

전체 snapshot은 약 1.55GiB이므로 실습 전에 disk budget과 Git LFS/Xet download 동작을 확인해야 합니다.

### 4. Label 구조

#### Ground truth detections

COCO bbox와 polygon segmentation을 `fo.Detections`로 변환했습니다. 29개 정의 class 중 현재 `frames.json`에서 실제 detection이 관측되는 class는 26개입니다. 가장 많은 class는 `lane_line`, `dashed_white_line`, `Pavement Striping`, `solid_yellow_line`, `Pedestrian Crossing` 등입니다.

동적 객체 annotation dataset으로 오해하면 안 됩니다. class는 주로 HD map의 도로 시설에서 유도됐고 vehicle·pedestrian 같은 동적 객체는 annotation 대상이 아닙니다.

#### HD map

Camera_0~4의 모든 560 labeled frame에 polyline이 있습니다. Camera_5는 top-view geometry 때문에 제외됐습니다. Lanelet2 좌표와 trajectory/point-cloud 좌표가 처음부터 동일하지 않아 geodetic origin을 거쳐 EPSG:6677로 재투영합니다.

#### Trajectory

GNSS/IMU pose stream은 200Hz지만 이 repository에는 front camera인 Camera_0 frame에 투영된 2D polyline으로 저장됩니다. 4 episode의 source frame 합계인 112 frame에 존재합니다.

#### Point cloud

원 source의 약 35M-point aggregated LiDAR scene에서 episode trajectory 30m 주변을 subset으로 만듭니다. 실시간 frame-by-frame LiDAR가 아니며 실제 RGB variation도 없어 height-based coloring을 기본으로 사용합니다.

### 5. 설치와 열기

전체 dataset을 받을 경우:

```bash
pip install -U fiftyone huggingface_hub
```

```python
import fiftyone as fo
from huggingface_hub import snapshot_download

path = snapshot_download(
    repo_id="Voxel51/hard-intersection-multimodal-sample",
    repo_type="dataset",
    local_dir="hard-intersection-data",
)

dataset = fo.Dataset.from_dir(
    dataset_dir=path,
    dataset_type=fo.types.FiftyOneDataset,
    name="hard_intersection_multimodal_sample",
)
session = fo.launch_app(dataset)
session.wait()
```

metadata만 먼저 받으려면 `allow_patterns`를 사용해 1.66GB media download를 피합니다.

```python
snapshot_download(
    repo_id="Voxel51/hard-intersection-multimodal-sample",
    repo_type="dataset",
    local_dir="hard-intersection-metadata",
    allow_patterns=["README.md", "fiftyone.yml", "metadata.json", "samples.json"],
)
```

## 데이터 품질과 주의점

### 연구 설계

- 한 교차로와 4 episode뿐이므로 geographic generalization을 평가할 수 없습니다.
- 같은 group의 camera slice를 train/test로 나누면 심각한 leakage입니다.
- source scene과 timestamp가 공유되므로 leave-one-episode-out도 완전한 location generalization은 아닙니다.
- aggregated point cloud를 temporal LiDAR benchmark로 사용하면 안 됩니다.
- Camera_5와 auxiliary +15-degree camera의 annotation 조건이 다릅니다.

### Annotation

- semantic label은 사람 annotation이 아니라 Grounding DINO, OneFormer, ViTMatte와 HD map alignment를 이용한 algorithmic output입니다.
- card frontmatter의 `annotations_creators: expert-generated`와 본문의 “human annotator 없음”을 함께 읽어야 합니다.
- 정의 class 29개와 현재 sample에서 관측되는 class 26개를 구분해야 합니다.
- `ground_truth` coverage 270/560은 labeled frame document 기준 48.2%입니다. 원 source image 896개를 분모로 쓰면 card의 약 30%가 됩니다.

### Privacy와 안전

- face mosaic와 license-plate masking은 완전하지 않을 수 있습니다.
- public-road 위치·trajectory·고해상도 image에는 재식별 위험이 남을 수 있습니다.
- 공개·재배포 전 frame-level privacy review와 추가 redaction이 필요합니다.
- 안전 benchmark 결과를 실제 차량 운행 안전 보증으로 해석하면 안 됩니다.

### License와 attribution

Dataset은 CC BY 4.0입니다. Dynamic Map Platform Co., Ltd.를 표시하고 source URL과 변경 사항을 기록해야 합니다. annotation 생성에 사용된 model·library는 각자 Apache-2.0 또는 MIT 조건을 가지며 weight나 source code가 이 repository에 포함된 것은 아닙니다.

## 용어 정리

| 용어 | 설명 |
|---|---|
| MMS | Mobile Mapping System, camera·LiDAR·GNSS·IMU를 차량에 통합한 측량 장비 |
| group slice | 같은 episode에 속한 camera 또는 3D media view |
| FO3D | FiftyOne의 3D scene description format |
| PCD | Point Cloud Data file format |
| HD map | lane·stop line·crosswalk 등을 정밀 좌표로 표현한 지도 |
| intrinsics | focal length와 principal point 같은 camera 내부 parameter |
| extrinsics | world와 camera 사이 pose transform |
| CRS | Coordinate Reference System, 좌표가 지구상 어디를 의미하는지 정의 |
| EPSG:6677 | 일본 평면직각좌표계 IX |
| leakage | 동일 장면 정보가 train과 test 양쪽에 들어가 평가가 부풀려지는 현상 |

## 실습 학습 가이드

- [`01_foundations.ipynb`](01_foundations.ipynb): repository manifest, group·slice, 용량과 coverage를 분석합니다.
- [`02_practice.ipynb`](02_practice.ipynb): 3D world point를 camera image에 투영하고 clipping합니다.
- [`03_advanced.ipynb`](03_advanced.ipynb): group-aware split, leakage와 label coverage audit를 설계합니다.

Notebook은 표준 Python만 사용하며 1.66GB dataset을 다운로드하지 않습니다. 확인된 metadata를 작은 toy data로 재현하므로 실제 model 성능 재현이 아닙니다.

## 다음 학습 경로

1. metadata-only snapshot으로 schema와 group slice를 확인합니다.
2. 전체 media를 받기 전에 disk·network·privacy policy를 검토합니다.
3. Camera_0의 trajectory와 HD map overlay를 눈으로 대조합니다.
4. group 단위 leave-one-episode-out baseline을 구성합니다.
5. source dataset의 별도 location을 확보해 location-held-out 평가로 확장합니다.
6. calibration perturbation, missing-camera, label-noise robustness를 측정합니다.
