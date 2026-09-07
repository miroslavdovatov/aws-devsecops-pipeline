FROM python:3.11-slim AS builder

WORKDIR /build

COPY app/requirements.txt .

RUN pip install --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY app .

ENV PATH=/root/.local/bin:$PATH

CMD ["fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]