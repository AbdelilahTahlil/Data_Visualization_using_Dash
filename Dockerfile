FROM python:3.10-buster

WORKDIR /enoviz

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . ./

CMD ["gunicorn", "--bind", "0.0.0.0:8050", "run_enoviz:flask_app"]
