# Set Base image
FROM python:3.6.11-slim

# Set working directory in the container
WORKDIR /app

# Copy all the file in current dir on this machine to the working dir in the container
ADD . /app

# install all the requirements
RUN pip install -r requirements.txt


# prepare the database # cassandra needed
CMD ["python", "prepare_db.py"]

# run the main flask service
CMD ["python", "run_server.py"]