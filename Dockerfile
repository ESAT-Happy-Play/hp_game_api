FROM python:3.8
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
WORKDIR /app
COPY . /app/
 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
 
EXPOSE 8000
EXPOSE 5432
 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]