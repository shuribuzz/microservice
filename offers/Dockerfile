FROM python:3.6

COPY ./requirements.txt /offers/requirements.txt
RUN apt-get update && pip install -r /offers/requirements.txt

WORKDIR /offers
COPY . /offers

EXPOSE 8001

CMD ["python", "run_offers.py"]