import argparse
import asyncio
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    # common console line arguments for application, 1st priority settings
    parser.add_argument('--postgres_user', dest='postgres_user', type=str)
    parser.add_argument('--postgres_password', dest='postgres_password', type=str)
    parser.add_argument('--postgres_database', dest='postgres_database', type=str)
    parser.add_argument('--postgres_address', dest='postgres_address', type=str)
    parser.add_argument('--kafka-bootstrap', dest='kafka_server', type=str)
    parser.add_argument('--offset-storage', dest='offset_storage', type=str)
    parser.add_argument('--data-storage', dest='data_storage', type=str)
    parser.add_argument('--zookeeper-host', dest='zookeeper_host', type=str)
    parser.add_argument('--zookeeper-port', dest='zookeeper_port', type=str)
    parser.add_argument('--redis-host', dest='redis_host', type=str)
    parser.add_argument('--redis-port', dest='redis_port', type=str)
    parser.add_argument('--cassandra_host', dest='cassandra-host', type=str)
    parser.add_argument('--cassandra_keyspace', dest='cassandra-keyspace', type=str)

    runserver_parser = subparser.add_parser('runserver')
    runserver_parser.add_argument('-a', '--address', default='0.0.0.0', dest='host', type=str)
    runserver_parser.add_argument('-p', '--port', default=8000, dest='port', type=int)

    subparser.add_parser('init_cassandra')
    subparser.add_parser('init_postgres')

    return parser.parse_args(sys.argv[1:])


def runserver(host='0.0.0.0', port=8000):
    from api.app import app
    app.run(host=host, port=port)


def override_configs(args):
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
