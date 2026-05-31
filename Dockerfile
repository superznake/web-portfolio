FROM python:3.12-slim
WORKDIR /app
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt
COPY . .
EXPOSE 62000
CMD ["python", "main.py"]