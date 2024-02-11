# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Copy the requirements.txt file into our working directory (/app)
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . . 

# Clone the repository (if still necessary)
# RUN git clone https://github.com/Hacklytics-24/DeathAnalyzer.git .

# Assuming the requirements are already satisfied by the previous pip install, 
# but if the cloned repo has additional requirements, uncomment the following line
# RUN pip3 install -r requirements.txt

EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

ENTRYPOINT ["streamlit", "run", "MapDeaths.py", "--server.port=8080", "--server.address=0.0.0.0"]
