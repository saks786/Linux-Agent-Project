from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask + Docker Compose + Jenkins + Postgres!"

@app.route("/db")
def db_check():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="db",  # service name in docker-compose.yml
            port=5432
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        conn.close()
        return f"✅ Connected to Postgres: {version}"
    except Exception as e:
        return f"❌ DB Connection failed: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
