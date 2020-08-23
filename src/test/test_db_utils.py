import unittest
import platform
import os

# module import work around
import sys
sys.path.append('../..')
from src.modules.db_utils import *

class test_db_utils(unittest.TestCase):
  def test_get_db_cred(self):
    hostname = platform.node()
    contents = get_db_cred('/etc/hostname')
    self.assertEqual(contents, hostname)

class Testdb_pool(unittest.TestCase):
  def setUp(self):
    self.conn_pool = db_pool(1, 2)

  def tearDown(self):
    self.conn_pool.cleanup()

  def test_read_data(self):
    user = self.conn_pool.read_data('SELECT user;')
    env_var = os.environ['DB_USER']
    self.assertEqual(env_var, user[0])

  def test_write_one(self):
    pass

  def test_write_many(self):
    pass
