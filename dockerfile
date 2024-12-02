FROM python:3.9-slim

WORKDIR /action

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "/action/fetch_rss.py"]
