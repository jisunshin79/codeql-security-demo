"""CodeQL 교육용: 의도적으로 보안 결함을 포함한 Flask 코드.

경고: 정적 분석만을 위한 예제입니다. 실행/배포/공개 서버 운영 금지.
"""

import hashlib
import os
import sqlite3
import subprocess

from flask import Flask, Response, jsonify, make_response, request

app = Flask(__name__)


# 1. SQL Injection: 사용자 입력을 SQL 문자열에 직접 결합
@app.get("/products")
def search_products():
    category = request.args.get("category", "")  # Source: 외부 입력
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE products (name TEXT, category TEXT)")
    connection.execute("INSERT INTO products VALUES ('Notebook', 'office')")
    query = "SELECT name FROM products WHERE category = '%s'" % category
    rows = connection.execute(query).fetchall()  # Sink: SQL 실행
    connection.close()
    return jsonify({"products": [row[0] for row in rows]})


# 2. Command Injection: 사용자 입력을 시스템 명령에 전달
@app.get("/diagnostics")
def diagnostics():
    command = request.args.get("command", "")  # Source
    output = subprocess.check_output(command, shell=True, text=True)  # Sink
    return jsonify({"output": output})


# 3. Path Traversal: 검증되지 않은 경로로 파일 열기
@app.get("/reports")
def read_report():
    filename = request.args.get("file", "")  # Source
    path = os.path.join("reports", filename)
    data = open(path, "rb").read()  # Sink
    return Response(data, mimetype="text/plain")


# 4. Reflected XSS: 사용자 입력을 HTML 응답에 그대로 반영
@app.get("/greeting")
def greeting():
    name = request.args.get("name", "")  # Source
    return make_response("<h1>Hello, " + name + "</h1>")  # Sink


# 5. Weak password hashing: 비밀번호에 MD5 사용
@app.post("/register")
def register():
    password = request.form.get("password", "")
    password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
    return jsonify({"message": "Hash calculated for teaching only"})


# 의도적으로 app.run()을 두지 않았습니다. 실행 없이 CodeQL로 분석하세요.
