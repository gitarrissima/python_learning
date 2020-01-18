import unittest
import sys
import os
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir + '\\..')
from log_analyser_configurator import LogAnalyserConfigurator


class LogAnalyserConfiguratorTests(unittest.TestCase):

    def test_get_config(self):
        default_config = {
            'log_dir': '.\\logs',
            'report_dir': '.\\reports',
            'report_size': 1000,
            'max_error_count': 100
        }
        configurator = LogAnalyserConfigurator(default_config, f'{cur_dir}\\data\\config')
        config = configurator.get_config()
        expected_config = {
            'log_dir': '.\\logs',
            'report_dir': '.\\reports',
            'report_size': 1000,
            'max_error_count': 3
        }
        self.assertEqual(config, expected_config)


if __name__ == '__main__':
    unittest.main()
