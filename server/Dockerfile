# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /server

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm

# Copy the entire project
COPY . .

# Start the Flask app
CMD ["python", "-u", "server.py"]
