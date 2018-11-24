FROM python:3.6-slim

COPY ./requirements.txt /offers/requirements.txt
RUN apt-get update && \
apt-get install --no-install-recommends -y build-essential && \
pip install -r /offers/requirements.txt

WORKDIR /offers
COPY . /offers

EXPOSE 8001

CMD ["python", "run_offers.py"]