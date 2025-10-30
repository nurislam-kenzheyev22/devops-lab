from flask import Flask, jsonify
import psycopg2, yaml

with open("/opt/app/config.yaml") as f:
    cfg = yaml.safe_load(f)

def conn():
    return psycopg2.connect(
        host=cfg["db"]["host"],
        port=cfg["db"]["port"],
        dbname=cfg["db"]["name"],
        user=cfg["db"]["user"],
        password=cfg["db"]["password"],
    )

app = Flask(__name__)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/users")
def users():
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("SELECT id,name,email FROM users ORDER BY id;")
            rows = cur.fetchall()
    return jsonify([{"id": r[0], "name": r[1], "email": r[2]} for r in rows])
