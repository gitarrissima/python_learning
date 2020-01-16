import argparse
from .log_analyser_configurator import LogAnalyserConfigurator
from .log_analyser_helper import LogAnalyserHelper
from .log_analyser import LogAnalyser


default_config = {
    'log_dir': '.\\logs',
    'report_dir': '.\\reports',
    'report_size': 1000
}

parser = argparse.ArgumentParser(description="Log analyser commandline parser")
parser.add_argument('--config', default='./config')
ns = parser.parse_args()

configurator = LogAnalyserConfigurator(default_config, ns.config)
config = configurator.get_config()

log_analyzer_helper = LogAnalyserHelper(config)
log_file_path = log_analyzer_helper.find_last_log_file()
report_file_path = log_analyzer_helper.calculate_report_file_path()
if log_analyzer_helper.check_report_file_already_exists():
    #TODO
    pass

if log_file_path.endswith('gz'):
    log_file_path = log_analyzer_helper.decompress_log_file()

log_analyzer = LogAnalyser(config, log_file_path, report_file_path)
log_analyzer.analyze_log()

