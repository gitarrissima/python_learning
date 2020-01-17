import unittest
import sys
import os
import filecmp
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir + '\\..')
from log_analyser import LogAnalyser


class LogAnalyserTests(unittest.TestCase):

    def test_analyse_log_success(self):
        log_path = f'{cur_dir}\\data\\logs\\nginx-access-ui.log'
        report_path = f'{cur_dir}\\data\\reports\\report.html'
        expected_report_path = f'{cur_dir}\\data\\reports\\report_expected.html'
        if os.path.exists(report_path):
            os.remove(report_path)
        config = {
            'report_size': 100
        }
        self.log_analyser = LogAnalyser(config,
                                        log_path,
                                        report_path)
        self.log_analyser.analyse_log()
        result = filecmp.cmp(report_path, expected_report_path)
        self.assertTrue(result)

    def test_analyse_log_max_error_count(self):
        config = {
            'report_size': 100,
            'max_error_count': 1
        }
        self.log_analyser = LogAnalyser(config,
                                        f'{cur_dir}\\data\\logs\\nginx-access-ui.log',
                                        f'{cur_dir}\\data\\reports\\report.html')
        try:
            self.log_analyser.analyse_log()
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
