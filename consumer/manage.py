import argparse
import asyncio
import sys

from api.app import app


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=bool, default=False)
    parser.add_argument('-c', type=bool, default=False)
    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':

    args = parse_args()

    if args.p:
        from common.database import init_postgres
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_postgres())
    if args.c:
        from common.database import init_cassandra
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_cassandra())
    else:
        app.run(host='localhost', port=5000)
