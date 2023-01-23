## async-task


<br>


### assign
```
title: 쿠폰 선착순 이벤트    

조건    
  1. python 프레임워크/DB 아무거나 사용할 것 (쿠폰 정보는 디비에 저장 필수)
  2. 비동기로 150명이 동시에 API콜을 요청(aiohttp, gather 메서드 활용할 것)
  3. 요청 순서대로 150명 중에 100명은 쿠폰을 획득하고, 나머지 50명은 쿠폰획득 실패 처리를 하는 API를 만들 것
  4. 쿠폰은 16자리의 임의의 문자열로 구성됨
  5. 단, 100명은 모두 다른 쿠폰을 발급받아야 함
```

<br>

### 사용한 스택
- Python 3.11
- FastAPI
- Postgresql (RDS)
- redis-server 7.0.7

<br>

### 서버 실행 방법
```zsh
$ python3 venv env
$ pip install -r requirements.txt

$ uvicorn src.apps.task.app:APP --reload
$ sh ./scripts/runserver.sh  # 스크립트로 실행 가능
```

<br>

### 실행 방법
```zsh
$ redis-server  # redis 실행
$ python main.py  # src/apps/task/api/coupon/main.py 실행 (client)
$ sh ./scripts/runserver.sh  # 서버 실행
```

** 실행에 필요한 환경변수
```text
MAIN_DB_HOST=
MAIN_DB_PORT=5432
MAIN_DB_DATABASE=
MAIN_DB_USER=
MAIN_DB_PASSWORD=

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DATABASE=0
```

<br>

### 과정

- redis 큐에 요청온 username 순차적으로 저장
- redis 큐 size 체크 후 100 이하인 경우 랜덤하게 발급한 쿠폰 부여
- DB에 저장
- 큐 size 100 초과하는 경우 쿠폰 소진 메시지 반환
