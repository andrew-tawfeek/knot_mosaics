FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install SageMath and dependencies
RUN apt-get update && \
    apt-get install -y \
    sagemath \
    python3-pip \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Flask and Flask-CORS
RUN sage -pip install flask flask-cors

WORKDIR /app

# Copy files
COPY wild_mosaics.py .
COPY classifier_utils.py .
COPY classifier_service.py .

EXPOSE 5001

# Run with sage python
CMD ["sage", "-python", "classifier_service.py"]