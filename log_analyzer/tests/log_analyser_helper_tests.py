import unittest
import sys
import os
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir + '\\..')
from log_analyser import LogAnalyserConfigurator


class LogAnalyserHelperTests(unittest.TestCase):

    def test_find_last_log_file(self):
        self.assertTrue(True)

    def test_calculate_report_file_path(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
