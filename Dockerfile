# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN pip3 uninstall -y Flask apscheduler
#RUN pip3 install --no-cache-dir setuptools==65.5.1
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install apscheduler==3.7
# supposed to be in requirements.txt as APScheduler~=3.10.2, but doesn't work

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
