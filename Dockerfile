FROM python:3.10-bookworm

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["python", "db_server_alejandroMacias.py"]
