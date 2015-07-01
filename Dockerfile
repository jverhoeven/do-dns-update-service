FROM		ubuntu:trusty
MAINTAINER	Jan Verhoeven

RUN			apt-get update && apt-get -y upgrade && apt-get install -y python-pip

RUN			mkdir -p /opt/do-dns-update-service
ADD			src/ /opt/do-dns-update-service/
RUN			chown -R www-data:www-data /opt/do-dns-update-service 
RUN			pip install -r /opt/do-dns-update-service/requirements.txt

EXPOSE		8000

CMD			cd /opt/do-dns-update-service && gunicorn do-dns-update-service:app
