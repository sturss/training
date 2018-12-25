import asyncio
import unittest

from common.zookeeper import ZookeeperManager


class TestZookeeperManager(unittest.TestCase):
    loop = asyncio.get_event_loop()

    def test_redis_save_get(self):
        test_value = 'test_value'
        self.loop.run_until_complete(ZookeeperManager.set_value('test_key', test_value))
        assert test_value == self.loop.run_until_complete(ZookeeperManager.get_value('test_key'))

    def test_redis_datatypes(self):
        string_value = 'test_value'
        self.loop.run_until_complete(ZookeeperManager.set_value('test_key', string_value))
        assert isinstance(self.loop.run_until_complete(ZookeeperManager.get_value('test_key')), str)

        int_value = 241
        self.loop.run_until_complete(ZookeeperManager.set_value('test_key', int_value))
        assert isinstance(self.loop.run_until_complete(ZookeeperManager.get_value('test_key')), int)

        float_value = 241.346
        self.loop.run_until_complete(ZookeeperManager.set_value('test_key', float_value))
        assert isinstance(self.loop.run_until_complete(ZookeeperManager.get_value('test_key')), float)

    def test_ensure_records(self):
        self.loop.run_until_complete(ZookeeperManager.ensure_record('new_test_key', 24.24))
        assert self.loop.run_until_complete(ZookeeperManager.get_value('new_test_key')) == 24.24
        self.loop.run_until_complete(ZookeeperManager.ensure_record('new_test_key', 212.55))
        assert self.loop.run_until_complete(ZookeeperManager.get_value('new_test_key')) == 24.24
        self.loop.run_until_complete(ZookeeperManager.ensure_record('non_existent_test_key'))
        assert self.loop.run_until_complete(ZookeeperManager.get_value('non_existent_test_key')) == 0

    @classmethod
    def tearDownClass(cls):
        cls.loop.run_until_complete(ZookeeperManager.remove('test_key'))
        cls.loop.run_until_complete(ZookeeperManager.remove('new_test_key'))
        cls.loop.run_until_complete(ZookeeperManager.remove('non_existent_test_key'))


if __name__ == '__main__':
    unittest.main()