FROM python:3
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /cs5774Project

COPY requirements.txt /cs5774Project/

RUN pip install --no-cache-dir -r requirements.txt
COPY cs5774Project/ /cs5774Project/

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]