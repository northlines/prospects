FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    cmake \
    protobuf-compiler \
    libprotobuf-dev \
    pkg-config \
    curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN curl -L https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz \
    -o /app/lid.176.ftz

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-k", "gevent", "-w", "4", "-b", "0.0.0.0:5000", "--error-logfile", "-", "main:app"]