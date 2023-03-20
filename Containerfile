FROM python:3.11-alpine
COPY . /src
RUN pip install kopf
RUN pip install kubernetes
CMD kopf run /src/event.py --verbose
