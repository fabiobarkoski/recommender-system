FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

COPY . .

# install deps
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["task", "run-prod"]
