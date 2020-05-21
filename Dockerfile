FROM ubuntu:18.04
RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv

RUN apt-get install -y libpq-dev python3-dev

RUN python3 -m virtualenv --python=/usr/bin/python3 /env

# Install dependencies:
COPY requirements.txt .

RUN . /env/bin/activate && pip install -r requirements.txt

# Run the application:
COPY myapp.py .
CMD . /env/bin/activate && ./manage.py runserver
