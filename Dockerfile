FROM python:3.8.0-alpine3.10

WORKDIR /home/asm

COPY . .

RUN pip install .

ENTRYPOINT ["sh"]