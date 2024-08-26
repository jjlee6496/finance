# 미주 분석 프로젝트

## 프로젝트 개요
이 프로젝트는 주식 데이터를 가져와 분석, 밸류에이션, 백테스팅을 수행하고 이를 통합적으로 관리할 수 있는 도구 제공을 목표로 한다. 이를 통하여 의사 결정에 도움을 주는 것을 목표로 한다. 

## 주요 기능

1. 주식 데이터 수집
2. 기본적 분석 및 기술적 분석
3. 기업 밸류에이션
4. 투자 전략 백테스팅
5. 포트폴리오 관리 및 성과 추적

## Docker Compose 사용
1. .env 파일 작성
```text
# postgres
DB_NAME={YOUR_DB_NAME}
DB_USER={USER_NAME}
DB_PASSWORD={PASSWORD}
DB_HOST={HOST}
DB_PORT={PORT}
```
2. docker-compose 실행
```bash
docker-compose up --build
```