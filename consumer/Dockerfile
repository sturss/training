FROM python:3.6
COPY requirements.txt /consumer/requirements.txt
WORKDIR /consumer/
RUN pip install $(grep -v "cassandra" requirements.txt)
RUN pip install cassandra-driver --install-option="--no-cython"