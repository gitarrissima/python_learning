import unittest
import sys
import os
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir + '\\..')
from log_analyser import LogAnalyser


class LogAnalyserTests(unittest.TestCase):
    def setUp(self):
        config = {
            'log_dir': '.\\data\\logs',
            'report_dir': '.\\data\\reports',
            'report_size': 100
        }
        self._log_analyser = LogAnalyser(config,
                                         '.\\data\\logs\\nginx-access-ui.log-20170630',
                                         '.\\data\\reports\\report-2017.06.30.html')

    def test_validate_log_parsing(self):
        self.assertFalse(self._log_analyser._validate_log_parsing('invalid', '1.123'))
        self.assertFalse(self._log_analyser._validate_log_parsing('/valid', 'invalid'))
        self.assertTrue(self._log_analyser._validate_log_parsing('/valid', '1.123'))


if __name__ == '__main__':
    unittest.main()
