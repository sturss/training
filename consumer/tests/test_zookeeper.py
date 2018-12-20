import unittest

from common.zookeeper import ZookeeperManager


class TestZookeeperManager(unittest.TestCase):
    def test_redis_save_get(self):
        test_value = 'test_value'
        ZookeeperManager.set_value('test_key', test_value)
        assert test_value == ZookeeperManager.get_value('test_key')

    def test_redis_datatypes(self):
        string_value = 'test_value'
        ZookeeperManager.set_value('test_key', string_value)
        assert isinstance(ZookeeperManager.get_value('test_key'), str)

        int_value = 241
        ZookeeperManager.set_value('test_key', int_value)
        assert isinstance(ZookeeperManager.get_value('test_key'), int)

        float_value = 241.346
        ZookeeperManager.set_value('test_key', float_value)
        assert isinstance(ZookeeperManager.get_value('test_key'), float)

    def test_ensure_records(self):
        ZookeeperManager.ensure_record('new_test_key', 24.24)
        assert ZookeeperManager.get_value('new_test_key') == 24.24
        ZookeeperManager.ensure_record('new_test_key', 212.55)
        assert ZookeeperManager.get_value('new_test_key') == 24.24
        ZookeeperManager.ensure_record('non_existent_test_key')
        assert ZookeeperManager.get_value('non_existent_test_key') == 0

    @classmethod
    def tearDownClass(cls):
        ZookeeperManager.connection.delete('test_key', recursive=True)
        ZookeeperManager.connection.delete('new_test_key', recursive=True)
        ZookeeperManager.connection.delete('non_existent_test_key', recursive=True)


if __name__ == '__main__':
    unittest.main()