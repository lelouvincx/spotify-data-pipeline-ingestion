# Dagster libraries to run both dagit and the dagster-daemon. Does not
# need to have access to any pipeline code.

FROM python:3.10-slim

# Set $DAGSTER_HOME and copy dagster instance and workspace YAML there
ENV DAGSTER_HOME=/opt/dagster/dagster_home
RUN mkdir -p $DAGSTER_HOME

WORKDIR $DAGSTER_HOME
COPY ./requirements.txt $DAGSTER_HOME
RUN pip install --upgrade pip && pip install -r requirements.txt
