import unittest

from common.redis import RedisManager


class TestRedisManager(unittest.TestCase):
    def test_redis_save_get(self):
        test_value = 'test_value'
        RedisManager.set_value('test_key', test_value)
        assert test_value == RedisManager.get_value('test_key')

    def test_redis_datatypes(self):
        string_value = 'test_value'
        RedisManager.set_value('test_key', string_value)
        assert isinstance(RedisManager.get_value('test_key'), str)

        int_value = 241
        RedisManager.set_value('test_key', int_value)
        assert isinstance(RedisManager.get_value('test_key'), int)

        float_value = 241.346
        RedisManager.set_value('test_key', float_value)
        assert isinstance(RedisManager.get_value('test_key'), float)

    def test_ensure_records(self):
        RedisManager.ensure_record('new_test_key', 24.24)
        assert RedisManager.get_value('new_test_key') == 24.24
        RedisManager.ensure_record('new_test_key', 212.55)
        assert RedisManager.get_value('new_test_key') == 24.24
        RedisManager.ensure_record('non_existent_test_key')
        assert RedisManager.get_value('non_existent_test_key') == 0

    @classmethod
    def tearDownClass(cls):
        RedisManager.connection.delete('test_key', 'new_test_key', 'non_existent_test_key')
        assert RedisManager.connection.get('test_key') is None
        assert RedisManager.connection.get('new_test_key') is None
        assert RedisManager.connection.get('non_existent_test_key') is None


if __name__ == '__main__':
    unittest.main()

