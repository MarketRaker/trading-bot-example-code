FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .env
COPY . /app/

#Enter the port number of the backend i.e. localhost:5005
EXPOSE 5005

#Enter the post number you want to forward i.e. localhost:5005
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5005", "--reload"]