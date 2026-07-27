FROM python:3.13-slim

LABEL maintainer="Tanmay Singh"
LABEL project="CloudPulse"
LABEL version="1.0.0"
LABEL org.opencontainers.image.title="CloudPulse"
LABEL org.opencontainers.image.description="Enterprise DevOps Demo"
LABEL org.opencontainers.image.source="https://github.com/Tanmay-hue/CloudPulse"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd -m cloudpulse

USER cloudpulse

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]