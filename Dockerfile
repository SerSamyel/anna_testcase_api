FROM Ubuntu

# Create the file repository configuration:
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update the package lists:
RUN apt-get update

# Install the latest version of PostgreSQL.
apt-get -y install postgresql-12

# Install python
RUN apt-get install python 3.8.5

# Upgrade pip
RUN pip install --upgrade pip

# Create work directory
CMD mkdir flask_api
WORKDIR flask_api

# Copy code
COPY ./anna_test_api

# Install python library
RUN pip install --no-cache-dir -r requirements.txt

# Set user, password and database name for postgresql
FROM /var/lib/postgresql/
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD admin
ENV POSTGRES_DB taskmaker

CMD
anna_test_api/manage.py db init &&
anna_test_api/manage.py db migrate "Initial migration." &&
anna_test_api/manage.py db upgrade

# Run
ENTRYPOINT FLASK_APP=/anna_test_api/app.py flask run