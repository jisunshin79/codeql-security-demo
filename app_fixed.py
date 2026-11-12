"""CodeQL 실습: app.py의 취약점을 개선한 비교용 코드.

교육용 참고 구현입니다. 실제 서비스라면 인증/접근 제어 등 추가 검토가 필요합니다.
"""

import sqlite3

from flask import Flask, abort, jsonify, make_response, request
from werkzeug.security import generate_password_hash

app = Flask(__name__)


# 1. SQL Injection 방지: 매개변수화된 쿼리
@app.get("/products")
def search_products():
    category = request.args.get("category", "")
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE products (name TEXT, category TEXT)")
    connection.execute("INSERT INTO products VALUES ('Notebook', 'office')")
    query = "SELECT name FROM products WHERE category = ?"
    rows = connection.execute(query, (category,)).fetchall()
    connection.close()
    return jsonify({"products": [row[0] for row in rows]})


# 2. Command Injection 방지: 셸 명령을 실행하지 않고 허용된 동작만 처리
@app.get("/diagnostics")
def diagnostics():
    action = request.args.get("command", "")
    results = {"health": "OK", "version": "demo-1.0"}
    if action not in results:
        abort(400)
    return jsonify({"output": results[action]})


# 3. Path Traversal 방지: 허용된 보고서명만 처리
REPORTS = {"summary.txt": "Sample summary", "guide.txt": "Sample guide"}


@app.get("/reports")
def read_report():
    filename = request.args.get("file", "")
    if filename not in REPORTS:
        abort(404)
    return make_response(REPORTS[filename], 200, {"Content-Type": "text/plain; charset=utf-8"})


# 4. Reflected XSS 방지: HTML 출력 시 이스케이프
@app.get("/greeting")
def greeting():
    from markupsafe import escape
    name = request.args.get("name", "")
    return make_response("<h1>Hello, " + str(escape(name)) + "</h1>")


# 5. 비밀번호 저장용 해시: 전용 KDF 사용
@app.post("/register")
def register():
    password = request.form.get("password", "")
    password_hash = generate_password_hash(password)
    return jsonify({"message": "Hash calculated for teaching only"})


# app.run() 없음: 실제 서비스 배포를 위한 완성품은 아닙니다.
