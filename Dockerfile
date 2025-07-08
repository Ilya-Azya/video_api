FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean
RUN pip install --default-timeout=100 -r requirements.txt

COPY . .

RUN chmod +x script.sh

CMD ["sh", "script.sh"]
