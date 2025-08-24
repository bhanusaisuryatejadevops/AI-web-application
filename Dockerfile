FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app

# non-root user
RUN useradd -m appuser
USER appuser

EXPOSE 8000
# Use 2 workers for demo; adjust via env
ENV GUNICORN_WORKERS=2
CMD ["bash", "-lc", "gunicorn --bind 0.0.0.0:${PORT} -w ${GUNICORN_WORKERS} app:app"]
