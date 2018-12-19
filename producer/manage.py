import argparse
import sys

from api.app import app


def override_configs(args):
    from api.config import Configs
    parameters = {k.upper(): v for k, v in args.__dict__.items() if k != 'command' and v is not None}
    Configs.update(parameters)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default='0.0.0.0', dest='host', type=str)
    parser.add_argument('-p', '--port', default=5000, dest='port', type=int)

    parser.add_argument('--kafka-bootstrap', dest='kafka_servers', type=str)

    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    args = parse_args()
    override_configs(args)
    app.run(host=args.host, port=args.port)
