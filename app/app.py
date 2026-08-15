from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres-service"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "appdb"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD")
    )


@app.get("/")
def home():
    return jsonify({
        "application": "Axion Ingestion Service",
        "status": "running"
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.get("/db-test")
def db_test():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT current_database(), version();")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "database": result[0],
            "postgres_version": result[1]
        })

    except Exception as e:
        return jsonify({
            "status": "database connection failed",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
