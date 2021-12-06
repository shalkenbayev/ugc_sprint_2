FROM python:3.9
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY ./src .
EXPOSE 8888

CMD uvicorn --port 8888 --host 0.0.0.0 main:app