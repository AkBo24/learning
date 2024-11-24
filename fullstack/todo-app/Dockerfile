FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN python3 -m venv venv \
ENV PATH="/usr/src/app/venv/bin:$PATH"
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
