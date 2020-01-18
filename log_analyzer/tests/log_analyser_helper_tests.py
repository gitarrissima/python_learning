import unittest
import sys
import os
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir + '\\..')
from log_analyser_helper import LogAnalyserHelper


class LogAnalyserHelperTests(unittest.TestCase):

    def setUp(self) -> None:
        config = {
            'log_dir': f'{cur_dir}\\data\\logs',
            'report_dir': f'{cur_dir}\\data\\reports'
        }
        self.log_analyser_helper = LogAnalyserHelper(config)
        self.last_log_path = self.log_analyser_helper.find_last_log_file()

    def test_find_last_log_file(self):
        self.assertEqual(self.last_log_path, f'{cur_dir}\\data\\logs\\nginx-access-ui.log-20170630')

    def test_calculate_report_file_path(self):
        report_path = self.log_analyser_helper.calculate_report_file_path()
        self.assertEqual(report_path, f'{cur_dir}\\data\\reports\\report-2017.06.30.html')


if __name__ == '__main__':
    unittest.main()
