FROM python:3.6

COPY ./requirements.txt /users/requirements.txt
RUN apt-get update && pip install -r /users/requirements.txt

WORKDIR /users
COPY . /users

EXPOSE 8000

CMD ["python", "run_users.py"]