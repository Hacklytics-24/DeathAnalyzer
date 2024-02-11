# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN pip install -r requirements.txt \ 
    apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Hacklytics-24/DeathAnalyzer.git .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "MapDeaths.py", "--server.port=8501", "--server.address=0.0.0.0"]