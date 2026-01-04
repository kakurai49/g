FROM python:3.11-slim

WORKDIR /app

ARG GIT_SHA=unknown
ARG BUILD_TIME

ENV GIT_SHA=${GIT_SHA}
ENV BUILD_TIME=${BUILD_TIME}
ENV PORT=8080
ENV APP_ENV=prod

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
