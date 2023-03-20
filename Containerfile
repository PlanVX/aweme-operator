FROM python:3.11
COPY . /src
RUN pip install kopf
CMD kopf run /src/event.py --verbose
