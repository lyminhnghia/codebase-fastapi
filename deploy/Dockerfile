# pull official base image
FROM python:3.12-slim

# set work directory
WORKDIR /opt

# set static environment variables
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# copy pip file
COPY requirements.txt .

# install dependencies
RUN pip install -U pip setuptools wheel &&\
  pip install -r requirements.txt

# copy project
COPY app/ app/
COPY config/ config/

# command: use exec-format over shell-format
ENTRYPOINT ["uvicorn", "--factory", "app:create_app"]
CMD ["--host=0.0.0.0", "--port=8000", "--workers=1", "--log-config=config/log-config.yml"]