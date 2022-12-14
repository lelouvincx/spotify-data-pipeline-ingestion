FROM jupyter/datascience-notebook:latest

# Set up location of container
WORKDIR /home/lelouvincx

# Install python requirements
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
