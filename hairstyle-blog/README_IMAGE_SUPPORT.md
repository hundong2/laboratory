# 헤어스타일 블로그 이미지 지원 시스템

이 업데이트로 헤어스타일 블로그에서 실제 이미지를 사용할 수 있게 되었습니다!

## 🖼️ 새로운 기능

### 1. 이미지 URL 지원
- AI 생성 이미지와 연예인 헤어스타일 이미지를 URL로 추가 가능
- 이미지 로드 실패 시 자동으로 placeholder로 fallback

### 2. 설정 파일 기반 관리
- `image_config.json` 파일을 통해 이미지 URL 관리
- 스타일별 개별 이미지 설정 가능
- 기본 이미지 설정으로 fallback 지원

## 📋 사용 방법

### 1. 이미지 설정 파일 편집
`hairstyle-blog/image_config.json` 파일을 편집하여 이미지 URL을 추가:

```json
{
  "ai_generated_images": {
    "레이어드 밥": "https://your-image-host.com/layered-bob.jpg",
    "커튼 뱅": "https://your-image-host.com/curtain-bang.jpg"
  },
  "celebrity_images": {
    "아이유 스타일": "https://your-image-host.com/iu-style.jpg",
    "태연 스타일": "https://your-image-host.com/taeyeon-style.jpg"
  },
  "default_image": {
    "ai_trend": "https://your-default-host.com/ai-default.jpg",
    "celebrity": "https://your-default-host.com/celebrity-default.jpg"
  }
}
```

### 2. 기사 생성
평소처럼 `generate_article.py`를 실행하면 설정된 이미지가 자동으로 포함됩니다:

```bash
python generate_article.py
```

### 3. 이미지 매칭 규칙
- **정확 매칭**: 설정 파일의 키와 정확히 일치하는 스타일명
- **부분 매칭**: 키나 스타일명에 포함된 부분 문자열
- **기본 이미지**: 매칭되는 이미지가 없을 때 default_image 사용
- **Placeholder**: 모든 것이 실패할 때 기존 placeholder 표시

## 🔧 고급 설정

### 이미지 호스팅 옵션
1. **외부 서비스**: Imgur, Cloudinary, AWS S3 등
2. **로컬 서버**: 같은 서버에 이미지 폴더 생성
3. **CDN**: 빠른 로딩을 위한 CDN 서비스

### 권장 이미지 규격
- **크기**: 400x300px (4:3 비율)
- **포맷**: JPG, PNG, WebP
- **파일 크기**: 100KB 이하 권장

## 🛠️ 예시 사용법

### 1. 로컬 이미지 호스팅
```bash
# 이미지 폴더 생성
mkdir hairstyle-blog/images

# 이미지 파일 추가
cp your-images/* hairstyle-blog/images/

# 설정 파일에서 로컬 경로 사용
"레이어드 밥": "./images/layered-bob.jpg"
```

### 2. 무료 이미지 서비스 활용
- **Unsplash**: `https://images.unsplash.com/photo-[ID]`
- **Placeholder.com**: `https://via.placeholder.com/400x300`
- **Lorem Picsum**: `https://picsum.photos/400/300`

## 🔍 트러블슈팅

### 이미지가 표시되지 않을 때
1. **URL 확인**: 이미지 URL이 접근 가능한지 확인
2. **CORS 정책**: 외부 이미지 서비스의 CORS 정책 확인
3. **파일 형식**: 지원되는 이미지 형식인지 확인
4. **네트워크**: 인터넷 연결 상태 확인

### 설정 파일 오류
```bash
# JSON 문법 검사
python -m json.tool image_config.json
```

## 📝 업데이트 내역

### v2.0.0 - 이미지 지원 추가
- ✅ 실제 이미지 URL 지원
- ✅ 자동 fallback 시스템
- ✅ 이미지 로드 실패 처리
- ✅ 설정 파일 기반 관리
- ✅ 기존 기능과 완전 호환

이제 여러분의 헤어스타일 블로그에 실제 이미지를 추가하여 더욱 생동감 있는 콘텐츠를 만들어보세요! 🎨✨