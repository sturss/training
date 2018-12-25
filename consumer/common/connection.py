
class Connection:
    @staticmethod
    def check_connection(f):
        async def wrapper(cls, *args, **kwargs):
            if cls.connection is None:
                await cls.connect()
            return await f(cls, *args, **kwargs)
        return wrapper
