FROM python:3.13-bookworm
COPY . /service_desk
RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r /service_desk/requirements.txt
WORKDIR /service_desk
EXPOSE 5000
