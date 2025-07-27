# FastAPI People API (Starter)

Невеликий FastAPI-сервер, який дозволяє додавати та переглядати людей. Перший крок до повноцінного API з PostgreSQL.

## 🚀 Запуск

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
