FROM python:3.6

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && rm requirements.txt

WORKDIR /app
COPY static static
COPY templates templates
COPY util util
COPY app.py app.py
COPY index.html index.html

EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0", "app:app"]