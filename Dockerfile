FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./app /app
COPY ./app/entrypoint.sh /entrypoint.sh
COPY ./requirements.txt /requirements.txt

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        tesseract-ocr \
        make \
        gcc

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r ../requirements.txt
RUN chmod +x entrypoint.sh
RUN ls

CMD ["./entrypoint.sh"]
