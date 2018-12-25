"""
    Module which launches application with user-made options
"""

import argparse
import asyncio
import sys


def parse_args():
    """
    Parses arguments given application on startup
    :return: Namespace object with parameters - dest's
    """
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    # common console line arguments for application, 1st priority settings (no command needed)
    parser.add_argument('--postgres_user', dest='postgres_user', type=str)
    parser.add_argument('--postgres_password', dest='postgres_password', type=str)
    parser.add_argument('--postgres_database', dest='postgres_database', type=str)
    parser.add_argument('--postgres_address', dest='postgres_address', type=str)
    parser.add_argument('--kafka-address', dest='kafka_address', type=str)
    parser.add_argument('--kafka-port', dest='kafka_port', type=int)
    parser.add_argument('--offset-storage', dest='offset_storage', type=str)
    parser.add_argument('--data-storage', dest='data_storage', type=str)
    parser.add_argument('--zookeeper-host', dest='zookeeper_host', type=str)
    parser.add_argument('--zookeeper-port', dest='zookeeper_port', type=int)
    parser.add_argument('--redis-host', dest='redis_host', type=str)
    parser.add_argument('--redis-port', dest='redis_port', type=int)
    parser.add_argument('--cassandra-host', dest='cassandra-host', type=str)
    parser.add_argument('--cassandra-keyspace', dest='cassandra-keyspace', type=str)
    parser.add_argument('--kafka-commit-seconds-interval', dest='kafka_commit_seconds_interval', type=int)
    parser.add_argument('--kafka-commit-messages-interval', dest='kafka_commit_messages_interval', type=int)


    # parameters given after runserver command e.g.: python manage.py runserver -a=0.0.0.0 -p=5000
    runserver_parser = subparser.add_parser('runserver')
    runserver_parser.add_argument('-a', '--address', default='0.0.0.0', dest='host', type=str)
    runserver_parser.add_argument('-p', '--port', default=8000, dest='port', type=int)

    subparser.add_parser('init_cassandra')
    subparser.add_parser('init_postgres')

    return parser.parse_args(sys.argv[1:])


def runserver(host='0.0.0.0', port=8000):
    """
    Runs application on a given socket or on a default one
    :param host: host ip address to run application on (str)
    :param port: port to use for application (int)
    :return: None
    """
    from api.app import app
    app.run(host=host, port=port)


def override_configs(args):
    """
    Takes from a Namespace object arguments defined by user i.e. those that are not None
    and overrides Configs with them
    :param args: Namespace object
    :return: None
    """
    from api.config import Configs
    parameters = {k.upper(): v for k, v in args.__dict__.items() if k != 'command' and v is not None}
    Configs.update(parameters)


if __name__ == '__main__':
    args = parse_args()

    override_configs(args)

    if args.command == 'init_postgres':
        from common.database import init_postgres
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_postgres())
    elif args.command == 'init_cassandra':
        from common.database import init_cassandra
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_cassandra())
    elif args.command == 'runserver':
        runserver(args.host, args.port)
    else:
        runserver()
