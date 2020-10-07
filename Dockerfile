FROM ubuntu:bionic

# Install wget, sudo
RUN apt-get update && apt-get upgrade && apt-get clean all && apt-get install wget sudo apt-utils gnupg -y 

# Create the file repository configuration:
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt bionic-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
ENV TZ=Europe/Moscow
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - > /dev/null

# Update the package lists:
RUN apt-get update

# Install the latest version of PostgreSQL.
RUN apt-get -y install postgresql-12

# Install python
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.8 -y

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Create work directory
CMD mkdir flask_api
WORKDIR flask_api

# Install git
RUN apt-get install git -y

# Copy code
RUN git clone https://github.com/SerSamyel/anna_testcase_api.git

# Install python library
RUN python3 -m pip install --no-cache-dir -r anna_test_api/requirements.txt

# Set user, password and database name for postgresql
FROM /var/lib/postgresql/
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD admin
ENV POSTGRES_DB taskmaker

# Create database
RUN python anna_test_api/manage.py db init && \
    python anna_test_api/manage.py db migrate "Initial migration." && \
    python anna_test_api/manage.py db upgrade

# Run
ENTRYPOINT FLASK_APP=/anna_test_api/app.py flask run
