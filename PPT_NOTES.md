# PPT용 구성 및 발표 멘트 — CodeQL 실습

## 슬라이드 A: CodeQL 실습 목적과 대상
**헤드메시지:** 단일 Python 웹서비스에서 서로 다른 5가지 보안 위험을 의도적으로 포함하고 CodeQL의 탐지 범위 검증

- 실습 대상: Flask 기반 간단한 웹서비스 코드(`app.py`)
  - 상품 검색 / 운영 진단 / 보고서 조회 / 인사말 출력 / 회원가입
- 분석 환경: 공개 GitHub Repository + CodeQL Default Setup (Python)
  - VS Code 및 CodeQL 프로그램 설치 없이 GitHub 웹에서 검사
- 탐지 목표: SQL Injection, 명령 주입, 경로 조작, XSS, 취약한 비밀번호 해시
- 실습 결과: **실제 분석 후 경고 유형·개수·위치를 입력해야 함**

**발표 멘트:** "이전 실습에서는 GitHub 자동화 파일의 권한 설정 문제만 확인했습니다. 이번에는 CodeQL이 실제 프로그램 코드에서 어떤 취약점을 분석하는지 알아보기 위해 작은 Python 웹서비스를 만들고, 서로 다른 보안 문제 다섯 가지를 넣었습니다."

## 슬라이드 B: CodeQL 분석 원리와 보안 경고
**헤드메시지:** 사용자 입력이 위험한 작업으로 연결되는 흐름을 추적해 취약점 위치와 원인 확인

- SQL Injection 예시
  - Source: `request.args.get('category')` — 외부 입력
  - Flow: 입력값을 `SELECT ...` SQL 문자열에 결합
  - Sink: `connection.execute(query)` — 데이터베이스에 전달
- CodeQL 분석: 소스코드 구조·흐름을 데이터베이스로 만들고 보안 쿼리 실행
- 결과 확인: Code Scanning Alert에서 규칙 ID, 코드 위치, 위험도, `Show paths` 확인

**화면:** `app.py` SQL 결합 부분 + CodeQL 경고 상세 (실제 캡처 후 삽입)

**발표 멘트:** "예를 들어 상품 검색어가 들어온다고 가정하겠습니다. 입력받은 검색어를 SQL 문장에 그대로 붙이면 원래 의도하지 않은 데이터 조회가 가능해질 수 있습니다. CodeQL은 입력값이 어디서 들어와 어떤 과정을 거쳐 SQL 실행 함수로 전달되는지 분석합니다."

## 슬라이드 C: 실제 탐지 결과 및 수정 전후 비교
**헤드메시지:** 유형별로 탐지 결과를 구분하고 코드 수정 후 재분석하여 검증 가능

| 문제 유형 | 공식 규칙 ID | 탐지 결과(입력) | 개선 방식 |
|---|---|---|---|
| SQL Injection | `py/sql-injection` | 실습 후 입력 | 매개변수화된 SQL 쿼리 |
| Command Injection | `py/command-line-injection` | 실습 후 입력 | 셸 호출 제거·허용 목록 |
| Path Traversal | `py/path-injection` | 실습 후 입력 | 파일명 허용 목록·경로 검증 |
| XSS | `py/reflective-xss` | 실습 후 입력 | HTML 특수문자 이스케이프 |
| Weak hash | `py/weak-sensitive-data-hashing` | 실습 후 입력 | 비밀번호 전용 해시 함수 |

- 수정 전: 의도적인 취약점이 포함된 `app.py`
- 수정 후: `app_fixed.py`와 동일하게 `app.py`를 개선한 다음 재분석
- 해석 주의: 정적 분석은 모든 취약점을 보장하지 않고 오탐·미탐 가능

**발표 멘트:** "실제 분석에서는 하나의 문제를 여러 번 잡아낸 결과가 아니라 서로 다른 유형의 위험을 구분해 확인하겠습니다. 그리고 코드 수정 전후 경고가 어떻게 바뀌는지 비교해 CodeQL이 개발 과정에서 어떤 역할을 하는지 설명할 수 있습니다."
