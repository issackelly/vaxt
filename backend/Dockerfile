FROM revolutionsystems/python:3.6.6-wee-optimized-lto

ENV PYTHONUNBUFFERED 1

ADD requirements.txt /requirements.txt

#Needed in the future, when we might do postgresql + GIS Extensions
#RUN apt-get update && apt-get upgrade -y && apt-get install -y build-essential libxmlsec1-dev binutils libproj-dev gdal-bin

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# Copy application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
ADD ./ /code/backend/
WORKDIR /code/backend

CMD python manage.py runserver 8000
