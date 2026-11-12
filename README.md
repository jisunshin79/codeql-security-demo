# GitHub CodeQL 정적 보안 분석 데모

> **교육 목적 전용.** 이 저장소의 `app.py`에는 보안 취약점이 의도적으로 포함되어 있습니다. 실제 서버에서 실행하거나 인터넷에 배포하지 마세요. 이 실습은 프로그램 실행 없이 GitHub의 **CodeQL Code Scanning**만 사용합니다.

## 데모의 목적

기존의 GitHub Actions 워크플로 권한 경고가 아니라, **실제 소스코드에서 5가지 서로 다른 보안 취약점**을 분석합니다. `app.py`는 결함 버전, `app_fixed.py`는 비교용 개선 버전입니다.

| 번호 | 파일/함수 | 문제 유형 | CodeQL 공식 규칙 ID | 주요 확인 사항 |
|---|---|---|---|---|
| 1 | `app.py` / `search_products` | SQL Injection | `py/sql-injection` | 사용자 입력 → SQL 문자열 → 데이터베이스 실행 |
| 2 | `app.py` / `diagnostics` | Command Injection | `py/command-line-injection` | 사용자 입력 → 시스템 명령 실행 |
| 3 | `app.py` / `read_report` | Path Traversal | `py/path-injection` | 사용자 입력 → 파일 경로 → 파일 열기 |
| 4 | `app.py` / `greeting` | Reflected XSS | `py/reflective-xss` | 사용자 입력 → HTML 응답 |
| 5 | `app.py` / `register` | Weak password hashing | `py/weak-sensitive-data-hashing` | 비밀번호 저장에 MD5 사용 |

> **주의:** 표의 항목은 CodeQL 공식 쿼리에 대응하는 *탐지 목표*입니다. 이 저장소를 실제 CodeQL 서비스에서 실행해 결과를 확인한 것은 아닙니다. 분석 엔진·버전·규칙 설정에 따라 탐지 항목과 개수가 달라질 수 있습니다. **반드시 실제 경고 화면으로 검증한 후 발표하세요.**

## GitHub에 올리는 가장 간단한 방법 (VS Code/터미널 불필요)

1. 이 ZIP 파일을 **압축 해제**합니다. ZIP 자체를 GitHub에 올리면 안 됩니다.
2. GitHub에서 새 **Public** 저장소를 생성합니다. 예: `codeql-security-demo`.
3. 저장소의 `Add file` → `Upload files`에 압축을 푼 폴더의 **모든 파일**(`app.py`, `app_fixed.py`, `README.md`, `requirements.txt`, `.gitignore`, `PPT_NOTES.md`)을 추가하고 `Commit changes`를 클릭합니다. `.gitignore`는 Finder에서 숨김파일 표시를 켜야 보일 수 있습니다. 꼭 필요하지는 않습니다.
4. `Settings` → `Advanced Security` → `CodeQL analysis` → `Set up` → `Default` → `Enable CodeQL`.
5. 설정 창의 **Languages에 Python이 표시되는지** 확인하세요. `GitHub Actions`만 표시된다면 Python 코드가 저장소에 업로드되었는지 먼저 확인합니다.
6. `Actions` 탭에서 분석 완료를 확인한 다음 `Security and quality` → `Code scanning`에서 알림을 확인합니다.
7. SQL Injection 등의 경고를 눌러 문제 위치, 공식 규칙, `Show paths`(표시될 경우)를 캡처합니다.

**추천:** 새 저장소를 만들어 쓰세요. 기존 `github_codeql_tutorial`은 GitHub Skills/Training의 채점 워크플로가 포함되어 있으므로 분석에 불필요한 권한 경고가 함께 나올 수 있습니다.

## 수정 전후를 보여주는 방법

- 먼저 `main` 브랜치의 `app.py`를 분석하여 실제 경고를 기록합니다.
- GitHub에서 `fix-codeql-demo` 브랜치를 만들고, `app_fixed.py` 내용을 `app.py`에 붙여 넣어 교체합니다. 변경 사항을 커밋합니다.
- `fix-codeql-demo` → `main` 방향으로 **Pull Request(PR)**를 엽니다. PR은 변경한 코드를 정식 브랜치에 합치기 전 검토를 요청하는 기능입니다.
- 수정 후 브랜치 및 PR의 CodeQL 결과를 확인합니다. 기존 경고가 자동으로 닫히는지 확인하려면 실제로 병합한 다음 기본 브랜치에 대한 분석 결과까지 확인해야 할 수 있습니다.
- **주의:** 브랜치별 경고와 PR의 새 경고는 표시 방식이 다를 수 있습니다. 경고 감소를 보이지 않는 경우 '개선 완료'로 표시하지 마세요.

## 공식 출처

- CodeQL 기본 설정: https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning
- SQL Injection: https://codeql.github.com/codeql-query-help/python/py-sql-injection/
- Command Injection: https://codeql.github.com/codeql-query-help/python/py-command-line-injection/
- Path Traversal: https://codeql.github.com/codeql-query-help/python/py-path-injection/
- XSS: https://codeql.github.com/codeql-query-help/python/py-reflective-xss/
- Weak password hashing: https://codeql.github.com/codeql-query-help/python/py-weak-sensitive-data-hashing/

## 발표 자료 작성

`PPT_NOTES.md`에 슬라이드별 제목, 설명 문구, 촬영할 화면, 발표 멘트를 넣었습니다.
