FROM python:3.10-slim

# Add repository code
WORKDIR /opt/dagster/app
COPY requirements.txt /opt/dagster/app
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 4000

# CMD allows this to be overridden from run launchers or executors that want
# to run other commands against your repository
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "repos.py"]
