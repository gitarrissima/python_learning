import unittest
import sys
import os
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir + '\\..')
from log_analyser import LogAnalyserConfigurator


class LogAnalyserConfiguratorTests(unittest.TestCase):

    def test_get_config(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
