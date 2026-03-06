FROM python:3.10

RUN apt-get update

COPY . /postgres_python

WORKDIR /postgres_python

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn

ENTRYPOINT ["uvicorn", "main:app", "--host" , "0.0.0.0", "--port", "8080"]
# Copy in the source code
COPY . .
EXPOSE 8000

# Setup an app user so the container doesn't run as the root user
#RUN useradd app
#USER app

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]