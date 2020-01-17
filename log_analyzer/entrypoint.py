import argparse
import logging
import sys
from log_analyser_configurator import LogAnalyserConfigurator
from log_analyser_helper import LogAnalyserHelper
from log_analyser import LogAnalyser

default_config = {
    'log_dir': '.\\logs',
    'report_dir': '.\\reports',
    'report_size': 1000,
    'max_error_count': 100
}
parser = argparse.ArgumentParser(description="Log analyser commandline parser")
parser.add_argument('--config', default='./config')
parser.add_argument('--log_file', default=None)
parser.add_argument('--log_level', default=logging.INFO, choices=[logging.INFO, logging.ERROR])
ns = parser.parse_args()

logging.basicConfig(filename=ns.log_file, filemode='w', level=ns.log_level,
                    format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
logger = logging.getLogger(__name__)

try:
    configurator = LogAnalyserConfigurator(default_config, ns.config)
    config = configurator.get_config()

    log_analyzer_helper = LogAnalyserHelper(config)
    log_file_path = log_analyzer_helper.find_last_log_file()
    if not log_file_path:
        logger.info(f'No log found to process')
        sys.exit(0)
    else:
        logger.info(f'Found log file to process: {log_file_path}')

    report_file_path = log_analyzer_helper.calculate_report_file_path()

    if log_analyzer_helper.check_report_file_already_exists():
        logger.info(f'Latest log {log_file_path} was already processed. Report is here: {report_file_path}')
        sys.exit(0)

    if log_file_path.endswith('gz'):
        log_file_path = log_analyzer_helper.decompress_log_file()

    log_analyser = LogAnalyser(config, log_file_path, report_file_path)
    log_analyser.analyse_log()
    logger.info(f'Job\'s done. Find report here: {report_file_path}')
except Exception as e:
    logging.exception(e)
    sys.exit(1)
