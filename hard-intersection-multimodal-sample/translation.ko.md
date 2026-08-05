# Hard Intersection Multimodal Sample 한국어 재구성본

작성일: 2026-08-06

## 원문 정보와 번역 범위

- 원문: [Voxel51 dataset card](https://huggingface.co/datasets/Voxel51/hard-intersection-multimodal-sample)
- source: [Dynamic Map Platform dataset](https://huggingface.co/datasets/dynamic-maps/hard-intersection-multimodal-sample)
- Voxel51 revision: `c9be8ed61671e518c9b57c90b5bc2b8c4b8dd3b6`
- 최종 확인 URL: `https://huggingface.co/datasets/Voxel51/hard-intersection-multimodal-sample`
- 원문 언어: 영어
- license: CC BY 4.0
- 접근일: 2026-08-06

이 파일은 dataset card의 구조와 의미를 따른 한국어 번역·학습용 재구성본입니다. 원문 전문을 복제하지 않고 핵심 정보, 수치와 경고를 보존해 설명합니다. API와 native metadata를 대조해 card만으로 드러나지 않는 차이도 `검수 메모`로 표시합니다.

## Dataset 상세

### 설명

Hard Intersection Multimodal Sample은 일본 도쿄 다카나와다이의 사고 위험이 높은 비정형 6거리 교차로를 industrial MMS로 촬영한 multimodal dataset입니다. 동기화된 multi-camera video, LiDAR point cloud, vehicle trajectory, 여러 형식의 HD map과 semantic annotation을 autonomous-driving 연구용으로 제공합니다.

이 교차로에는 언덕 정상의 blind spot, 급한 curve, 좁은 도로, centerline을 넘는 차량, 복잡한 traffic signal이 함께 존재합니다.

- curation·funding·sharing: Dynamic Map Platform Co., Ltd.
- documentation language: English
- license: CC BY 4.0

### Source

Voxel51 repository는 Dynamic Map Platform의 더 큰 source dataset을 FiftyOne native grouped format으로 다시 구성한 sample입니다. 연결된 3DGS viewer와 source dataset은 별도 Hugging Face repository이므로 크기와 file structure를 혼동하지 않아야 합니다.

## 사용 목적

### 권장 용도

- 복잡한 urban intersection의 multi-camera perception
- HD map과 sensor observation을 결합하는 map-aware perception
- road infrastructure semantic segmentation
- 어려운 scene의 localization과 trajectory 분석
- point-cloud semantic understanding과 3D visualization
- panorama perception과 3D reconstruction workflow
- sensor observation에 대한 HD map projection 검증
- autonomous-driving edge-case pipeline의 safety-oriented test

Calibration을 포함하므로 multi-view geometry를 연습할 수 있고, trajectory와 point cloud는 sensor-fusion 연구의 출발점이 됩니다.

### 범위 밖 용도

- 한 지점뿐이므로 넓은 geographic coverage 연구
- aggregated PCD를 사용한 실시간 LiDAR sequence 처리
- custom projection 없이 HD map format 간 consistency를 가정하는 연구
- 추가 privacy 검수 없는 민감 정보 활용
- 실제 차량의 안전 인증 또는 deployment 보증

## Dataset 구조

이 자료는 4개 group으로 구성된 FiftyOne dataset이며 `media_type`은 `group`, 기본 slice는 `Camera_0`입니다. 각 group은 한 번의 교차로 주행 episode입니다.

### Topology

- 4 episode
- episode당 Camera_0~5 video 6개
- episode당 point-cloud FO3D scene 1개
- 총 28 sample: video 24개 + 3D 4개

Source image sequence 기준 episode frame 수는 28, 26, 30, 28입니다. MP4 metadata는 각 값보다 하나 많은 29, 27, 31, 29를 보고하므로 label과 decode frame alignment를 확인해야 합니다.

### Sample field

| Field | 의미 |
|---|---|
| `filepath` | MP4 또는 FO3D 상대 경로 |
| `group` | 같은 episode의 slice를 연결하는 group identity |
| `episode_id` | 주행 episode 식별자 |
| `camera` | video slice의 Camera_0~5 |
| `metadata` | video 해상도·FPS·duration 또는 3D scene metadata |

### Frame field

| Field | FiftyOne label | 범위 |
|---|---|---|
| `ground_truth` | `Detections` | Camera_0~4 일부, 270 frame |
| `hd_map` | `Polylines` | Camera_0~4 전체, 560 frame |
| `trajectory` | `Polylines` | Camera_0만, 112 frame |

### Label 변환

#### COCO semantic annotation

Absolute bbox `[x, y, w, h]`를 image 크기로 나눠 relative coordinate로 변환하고 polygon segmentation을 보존합니다. Card는 29 class를 정의하지만 Voxel51 `frames.json`에서 실제 detection이 나타나는 class는 26개입니다. Camera_5와 4 episode 중 뒤의 2개에는 detection label이 없습니다.

#### Lanelet2 HD map

Lane boundary, centerline, stop line과 crosswalk를 camera view에 projection합니다. Lanelet2 local coordinate를 geodetic origin을 통해 EPSG:6677로 바꾸고 COLMAP world-to-camera extrinsics와 intrinsics를 적용합니다. Image 밖 segment는 clip하고 보이는 연속 구간으로 나눕니다.

#### Vehicle trajectory

200Hz GNSS/IMU pose stream 전체 경로를 Camera_0에만 2D polyline으로 투영합니다. 이것은 frame마다 새로 관측된 trajectory가 아니라 전체 driving path overlay입니다.

#### Point cloud와 FO3D

여러 run을 합친 scene point cloud에서 각 episode trajectory 30m 주변을 추출합니다. LAS를 RGB·intensity가 포함된 PCD로 바꾸고 FO3D scene이 이를 참조합니다. Source LAS의 색 variation이 없으므로 height coloring을 사용합니다.

### Video encoding

- H.264/avc1
- 2048×2464 portrait
- YUV420p, CRF 23
- 고정 FPS가 아니라 image timestamp에서 계산한 약 1.54~2.34 FPS

### Dataset metadata

- CRS: EPSG:6677
- episode: 4개
- group slice: Camera_0~5, point_cloud
- FiftyOne export version: 1.20.0

## Parsing 선택

1. Label과 3D scene을 native하게 연결하기 위해 MCAP 대신 grouped dataset을 선택했습니다.
2. 672개 source main-camera image를 24개 video sample로 encoding했습니다.
3. 전체 35M-point scene을 trajectory 주변으로 줄여 episode별 PCD를 만들었습니다.
4. 독립 timestamp와 annotation 부재 때문에 auxiliary `+15deg` camera를 제외했습니다.
5. Scene-level semantic point cloud는 episode별 label이 아니고 FiftyOne 3D semantic label 표현이 제한적이라 import하지 않았습니다.
6. Lanelet2와 EPSG:6677의 서로 다른 local coordinate를 명시적으로 reprojection했습니다.
7. COLMAP extrinsics를 world-to-camera transform으로 사용했습니다.
8. COCO integer category를 class name으로 변환했습니다.
9. Trajectory를 FO3D geometry가 아니라 Camera_0 frame label로 보존했습니다.

## Class

29개 정의 class는 road surface, lane line, white/yellow line, arrow, pedestrian crossing, stop bar, traffic light, information·warning sign, bus, wrong-way sign과 parking 등입니다. 대부분 HD map attribute에서 유도된 static road-infrastructure class이며 동적 vehicle·pedestrian annotation dataset이 아닙니다.

## Dataset 생성

### Curation 이유

다카나와다이는 blind spot, 6거리 topology, narrow road, multi-phase signal, dense traffic과 heavy occlusion이 한 지점에 모여 있어 extreme edge-case를 시험하기 위한 장소로 선택됐습니다.

### 수집

MMS에는 6개 동기 camera, multi-return LiDAR, 200Hz IMU/GNSS와 COLMAP-based calibration이 사용됐습니다. 좌표계는 도쿄 지역의 일본 평면직각좌표계 IX인 EPSG:6677입니다.

Point cloud와 3DGS는 여러 주행을 합친 static scene이며 dynamic object를 제거했습니다. 따라서 실제 traffic agent의 3D temporal motion을 복원하는 용도로는 적합하지 않습니다.

### Annotation

Semantic image label은 다음 model과 HD map alignment를 통해 algorithmically 생성됐습니다.

- Grounding DINO Base: zero-shot localization
- OneFormer Cityscapes Swin-L: segmentation polygon
- ViTMatte Base: boundary refinement

Semantic point cloud와 HD map도 자동 또는 proprietary mapping pipeline에서 생성됐으며 semantic label 생산에 human annotator는 참여하지 않았습니다. 3DGS에는 gsplat과 Splatfacto-W가 사용됐습니다.

### 개인정보

Face는 mosaic, license plate는 탐지된 범위에서 masking했습니다. Card는 anonymization이 완전하지 않을 수 있음을 명시합니다. 원본 frame을 공개·분석·재배포하기 전에 별도 privacy review가 필요합니다.

## 인용과 attribution

Dataset을 사용하면 Dynamic Map Platform Co., Ltd., 2026, Hugging Face dataset임을 표시하고 source URL을 연결합니다. Voxel51 sample을 사용했다면 Voxel51 repository revision과 변환·분석 변경 사항도 함께 기록하는 것이 재현에 유리합니다.

## 제한사항

- 한 교차로, 4 episode뿐임
- PCD는 multi-run aggregated scene임
- semantic detection은 source image 기준 일부만 존재
- Camera_5와 auxiliary camera는 annotation 조건이 다름
- map format별 coordinate representation이 다름
- anonymization이 완전하지 않을 수 있음
- algorithmic pseudo-label의 오류와 class bias가 남음
- 현재 sample만으로 location-held-out generalization을 측정할 수 없음

## 검수 메모

- Hugging Face API에서 public·non-gated 상태와 commit SHA를 확인했습니다.
- 재귀 tree API의 39개 file은 총 1,659,090,565 bytes입니다. Dataset metadata API의 `usedStorage`는 1,659,041,863 bytes로 48,702 bytes 차이가 나므로 endpoint와 revision을 함께 기록했습니다.
- `samples.json`에서 video 24개, 3D 4개와 group 4개를 확인했습니다.
- `frames.json`에서 `ground_truth` 270, `hd_map` 560, `trajectory` 112 frame을 확인했습니다.
- Detection은 총 6,854개이며 정의 29 class 중 26개가 실제 등장합니다.
- Dataset card의 source frame 수와 MP4 metadata frame 수가 각각 1씩 다른 점을 별도로 표시했습니다.

## 학습 자료

- [종합 분석](README.md)
- [기초 manifest·group 실습](01_foundations.ipynb)
- [3D-to-2D projection 실습](02_practice.ipynb)
- [Group split·coverage audit 실습](03_advanced.ipynb)
