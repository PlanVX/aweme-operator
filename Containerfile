FROM python:3.12-alpine
COPY . /src
RUN pip install kopf
RUN pip install kubernetes
CMD kopf run /src/event.py --verbose
