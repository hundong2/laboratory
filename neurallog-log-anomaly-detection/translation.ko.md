# NeuralLog GitHub README 한국어 학습 번역

작성일: 2026-07-23

## 원문 정보

- 원문 URL: [https://github.com/LogIntelligence/NeuralLog](https://github.com/LogIntelligence/NeuralLog)
- 최종 확인 URL: [https://github.com/LogIntelligence/NeuralLog](https://github.com/LogIntelligence/NeuralLog)
- 페이지 제목: `GitHub - LogIntelligence/NeuralLog: Log-based Anomaly Detection Without Log Parsing (ASE 2021, Research Track)`
- 원문 언어: 영어
- 접근일: 2026-07-23
- 확인 방식: clone/submodule 없이 GitHub 웹페이지, raw 파일, GitHub API 메타데이터만 확인
- 관련 논문: [Log-based Anomaly Detection Without Log Parsing](https://arxiv.org/abs/2108.01955)

이 문서는 GitHub README의 흐름을 유지하되 한국어 학습자가 이해하기 쉽게 번역·재구성한 자료다. 원문 전체를 그대로 복제하지 않고 핵심 내용, 명령, 결과 표의 의미를 보존했다.

## NeuralLog

NeuralLog 저장소는 ASE 2021 Research Track 논문 `Log-based Anomaly Detection Without Log Parsing`의 구현이다.

논문의 문제의식은 다음과 같다. 소프트웨어 시스템은 장애 분석과 운영 관리를 위해 많은 런타임 정보를 로그로 남긴다. 기존 연구들은 로그 데이터를 이용해 시스템 이상을 탐지하는 머신러닝 모델을 만들었다. 그러나 저자들의 실증 연구에 따르면 기존 로그 기반 이상 탐지 방법은 로그 파싱 오류에 크게 영향을 받는다. 주요 원인은 OOV 단어와 로그 의미의 오해다.

로그 파싱 오류는 이상 탐지에 중요한 정보를 잃게 만들 수 있다. 이를 해결하기 위해 저자들은 로그 파싱이 필요 없는 새로운 로그 이상 탐지 방식인 NeuralLog를 제안한다. NeuralLog는 원시 로그 메시지의 의미를 추출해 semantic vector로 표현한다. 그런 다음 이 벡터 시퀀스를 Transformer 기반 분류 모델에 넣어 이상을 탐지한다. Transformer는 로그 시퀀스의 문맥 정보를 포착할 수 있다.

README는 NeuralLog가 네 개 공개 데이터셋에서 모두 0.95 이상의 F1-score를 달성했고 기존 접근법보다 좋은 성능을 보였다고 설명한다.

## Framework

NeuralLog는 세 구성요소로 이루어진다.

| 단계 | 한국어 설명 |
| --- | --- |
| Preprocessing | 로그 메시지에서 특수문자와 숫자를 제거하고 텍스트를 정규화한다. |
| Neural Representation | BERT를 사용해 로그 메시지에서 semantic vector를 추출한다. |
| Transformer-based Classification | Positional Encoding과 Transformer Encoder를 포함한 분류 모델로 이상을 탐지한다. |

핵심은 로그 파싱 결과인 event ID나 template을 쓰지 않는다는 점이다. 원본 로그 텍스트를 신경망 표현으로 바꾸고, 시퀀스 모델이 정상/이상을 판정한다.

## Requirements

README 기준 요구 사항은 다음과 같다.

| 항목 | 버전 또는 패키지 |
| --- | --- |
| Python | 3.5 - 3.8 |
| TensorFlow | 2.4 |
| transformers | Hugging Face Transformers |
| tf-models-official | 2.4.0 |
| scikit-learn | 필요 |
| pandas | 필요 |
| numpy | 필요 |
| gensim | README 목록에는 포함되지만 현재 requirements.txt에는 보이지 않는다. |

원격 `requirements.txt`는 `numpy~=1.19.5`, `scikit-learn~=0.24.2`, `transformers~=4.19.2`, `tensorflow~=2.4.0`, `tf-models-official~=2.4.0`, `pandas~=1.4.2`를 한 줄에 적고 있다. 최신 Python에서는 TensorFlow 2.4 설치가 어려울 수 있으므로 재현 환경은 Python 3.8과 오래된 dependency를 별도 가상환경으로 구성하는 편이 안전하다.

## Demo

README는 두 단계 데모를 제시한다.

첫째, semantic vector를 추출한다. 예시는 `neurallog.data_loader`를 import하고, BGL 로그 파일을 지정한 뒤 `load_supercomputers` 함수로 train/test 데이터를 만든다. 주요 인자는 `train_ratio`, `windows_size`, `step_size`, `e_type='bert'`이다.

둘째, Transformer 모델을 학습하고 테스트한다. 자세한 과정은 `demo/Transformer_based_Classification.ipynb`와 `demo/NeuralLog.py`에 연결되어 있다.

BGL 전체 데모 흐름은 다음과 같다.

```bash
pip install -r requirements.txt
wget https://zenodo.org/record/3227177/files/BGL.tar.gz && tar -xvzf BGL.tar.gz
mkdir logs && mv BGL.log logs/.
cd demo
python NeuralLog.py
```

이 명령은 저장소를 이미 받은 상태를 전제로 한다. 이번 작업에서는 사용자의 요청에 따라 저장소를 clone하지 않았고, 실행도 수행하지 않았다.

## Data and Models

README는 데이터셋과 사전학습 모델을 Figshare 링크에서 찾을 수 있다고 안내한다. 또한 BGL 데이터는 Zenodo에서 받을 수 있는 명령을 제공한다.

데이터 처리 관점에서 저장소 구현은 두 종류의 window를 사용한다.

- HDFS: BlockId를 기준으로 같은 세션의 로그를 묶는다.
- BGL/Thunderbird/Spirit: 고정 길이 또는 sliding window로 로그를 묶고, window 안에 failure log가 있으면 anomaly로 라벨링한다.

## Results

README의 결과 표를 NeuralLog 중심으로 정리하면 다음과 같다.

| Dataset | Precision | Recall | F1-score |
| --- | --- | --- | --- |
| HDFS | 0.96 | 1.00 | 0.98 |
| BGL | 0.98 | 0.98 | 0.98 |
| Thunderbird | 0.93 | 1.00 | 0.96 |
| Spirit | 0.98 | 0.96 | 0.97 |

비교 대상에는 LR, SVM, Invariant Mining(IM), LogRobust, Log2Vec가 포함된다. README 결과에서는 NeuralLog가 네 데이터셋 모두에서 높은 F1-score를 보인다. 특히 BGL과 Thunderbird처럼 기존 baseline이 크게 흔들리는 데이터셋에서 파싱 없는 의미 표현의 장점이 두드러진다.

## Code Structure

clone 없이 GitHub API와 raw 파일로 확인한 구조는 다음과 같다.

```text
NeuralLog/
  README.md
  requirements.txt
  LICENSE
  demo/
    NeuralLog.py
    Transformer_based_Classification.ipynb
  neurallog/
    __init__.py
    data_loader.py
    utils.py
    models/
      __init__.py
      transformers.py
      positional_encodings.py
      logrobust.py
      log2vec.py
```

`neurallog/models/__init__.py`는 `transformer_classifer`를 `NeuralLog` 이름으로 내보낸다. `transformers.py`는 NeuralLog의 Transformer classifier를 구현하고, `logrobust.py`와 `log2vec.py`는 비교 모델 구현을 포함한다.

## Citation

원문 README는 연구에 코드와 모델이 도움이 되면 다음 논문을 인용하라고 안내한다.

```bibtex
@inproceedings{le2021log,
  title={Log-based anomaly detection without log parsing},
  author={Le, Van-Hoang and Zhang, Hongyu},
  booktitle={2021 36th IEEE/ACM International Conference on Automated Software Engineering (ASE)},
  pages={492--504},
  year={2021},
  organization={IEEE}
}
```

## 학습자 관점의 핵심 해석

NeuralLog는 로그 분석을 "템플릿 매칭 문제"에서 "짧은 기술 문장들의 시퀀스 분류 문제"로 바꾼다. 이 변화는 OOV와 파싱 오류에 강할 수 있지만, 모든 정보를 보존한다는 뜻은 아니다. 숫자 제거와 평균 풀링은 단순하고 효율적이지만, 특정 숫자 패턴이나 정확한 경로가 이상 탐지의 핵심인 도메인에서는 손실이 될 수 있다.

따라서 NeuralLog를 실제 운영에 적용하려면 다음을 확인해야 한다.

- 숫자와 특수문자 제거가 도메인에서 안전한가?
- train/test split이 시간 순서를 잘 반영하는가?
- 장애 로그가 희소한 class imbalance 상황에서 threshold가 적절한가?
- 사전학습 언어 모델이 해당 시스템 로그 어휘를 충분히 이해하는가?
- 신규 버전 배포 후 로그 문구가 바뀌어도 성능이 유지되는가?
