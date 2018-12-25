import asyncio
import unittest

from common.redis import RedisManager


class TestRedisManager(unittest.TestCase):
    loop = asyncio.get_event_loop()

    def test_redis_save_get(self):
        test_value = 'test_value'
        self.loop.run_until_complete(RedisManager.set_value('test_key', test_value))
        assert test_value == self.loop.run_until_complete(RedisManager.get_value('test_key'))

    def test_redis_datatypes(self):
        string_value = 'test_value'
        self.loop.run_until_complete(RedisManager.set_value('test_key', string_value))
        assert isinstance(self.loop.run_until_complete(RedisManager.get_value('test_key')), str)

        int_value = 241
        self.loop.run_until_complete(RedisManager.set_value('test_key', int_value))
        assert isinstance(self.loop.run_until_complete(RedisManager.get_value('test_key')), int)

        float_value = 241.346
        self.loop.run_until_complete(RedisManager.set_value('test_key', float_value))
        assert isinstance(self.loop.run_until_complete(RedisManager.get_value('test_key')), float)

    def test_ensure_records(self):
        self.loop.run_until_complete(RedisManager.ensure_record('new_test_key', 24.24))
        assert self.loop.run_until_complete(RedisManager.get_value('new_test_key')) == 24.24
        self.loop.run_until_complete(RedisManager.ensure_record('new_test_key', 212.55))
        assert self.loop.run_until_complete(RedisManager.get_value('new_test_key')) == 24.24
        self.loop.run_until_complete(RedisManager.ensure_record('non_existent_test_key'))
        assert self.loop.run_until_complete(RedisManager.get_value('non_existent_test_key')) == 0

    @classmethod
    def tearDownClass(cls):
        cls.loop.run_until_complete(RedisManager.connection.delete('test_key', 'new_test_key', 'non_existent_test_key'))
        assert cls.loop.run_until_complete(RedisManager.connection.get('test_key')) is None
        assert cls.loop.run_until_complete(RedisManager.connection.get('new_test_key')) is None
        assert cls.loop.run_until_complete(RedisManager.connection.get('non_existent_test_key')) is None


if __name__ == '__main__':
    unittest.main()

