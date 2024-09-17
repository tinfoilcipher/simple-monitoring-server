#--Selected for the low number of CVEs
FROM python:3.11-alpine3.19

#--Don't need to hear pip complaining about venvs if we're already in a container
ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONDONTWRITEBYTECODE=1

RUN adduser --system --no-create-home monitor_backend
WORKDIR /opt/app
RUN chmod 755 /opt/app

COPY ./src/*.py /opt/app/
COPY requirements.txt /opt/app/
RUN pip install -r requirements.txt

USER monitor_backend
CMD ["python", "app.py"]
