FROM python:3.10
EXPOSE 8010
RUN apt-get update
RUN apt-get install -y postgresql-client
WORKDIR /movies_admin/
COPY requirements.txt /movies_admin/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /movies_admin/
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8010"]

