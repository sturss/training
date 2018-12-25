# training
Kafka consumer/producer testing

<h2> 1. In Docker container </h2>
For starting application in Docker containers it's enough change directory to the folder with docker-compose.yml file and run command:

```yaml
    sudo docker-compose up
```

<h2> 2. Applciation on host machine </h2>
In application (consumer/producer) directory run command:

```yaml
    python manage.py runserver -a=0.0.0.0 -p=8000
```
-a (--address) and -p (--port) parameters are optional and may not be used. Server will start at default socket 127.0.0.1:8000 

<h2> 3. Settings </h2>
1. Set up virtual environment for runnign application, create a new environment with virtualenv (pytohn 3.6) and install all necessary dependencies from file requirements.txt.

2. Run command for creating database and all necessary tables

```yaml
    python manage.py init_postgres [init_cassandra] 
```
3. Configure application as you want. Configs may be set up in a dictionary Configs in configs.py file, in environment, where application will be run, or using console-line arguments. List of configs is following:
    * POSTGRES_ADDRESS: Address of postgres database server (default localhost)
    * POSTGRES_USER: Username of database user (default admin)
    * POSTGRES_PASSWORD: Password of database user (default admin)
    * POSTGRES_DATABASE: Database which will be used (default movies)
    * KAFKA_ADDRESS: IP-address of Kafka bootstrap (default localhost)
    * KAFKA_PORT: Port of for Kafka bootstrap (default 9092)
    * OFFSET_STORAGE: Service for storing offset of the last accepted message (default REDIS, may be ZOOKEEPER)
    * DATA_STORAGE: Service for storing messages that came from Kafka (default POSTGRES, may be CASSANDRA)
    * ZOOKEEPER_HOST: Address of Zookeeper service (default localhost)
    * ZOOKEEPER_PORT: Port of Zookeeper service (default 2181)
    * REDIS_HOST: Address of Redis service (default localhost)
    * REDIS_PORT' Port of Redus service (default 6379)
    * CASSANDRA_HOST: Address of Cassandra service (default localhost)
    * CASSANDRA_KEYSPACE: Keyspace to use in Cassandra (default movies) <br>
    * KAFKA_COMMIT_SECONDS_INTERVAL: Interval in seconds for kafka commit (default 10),
    * KAFKA_COMMIT_MESSAGES_INTERVAL: Interval in messages for kafka commit (default 10),
   Environment configuration also may be set up in docker-compose.yml file in environment list