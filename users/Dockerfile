FROM python:3.6-slim

COPY ./requirements.txt /users/requirements.txt
RUN apt-get update && \
apt-get install --no-install-recommends -y build-essential && \
pip install -r /users/requirements.txt

WORKDIR /users
COPY . /users

EXPOSE 8000

CMD ["python", "run_users.py"]