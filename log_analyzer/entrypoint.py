import argparse
import glob
import os
import datetime
import gzip
import shutil
from log_analyser_configurator import LogAnalyserConfigurator
from log_analyser import LogAnalyser


def find_last_log_file(config: dict) -> str:
    """ Function searches for latest log file in config.log_dir directory
        Returns name of file if it exists """

    log_filename_template = os.path.join(config['log_dir'], "nginx-access-ui.log-*")
    log_file_pathes = glob.glob(log_filename_template)
    if len(log_file_pathes) == 0:
        # TODO
        return
    latest_log = log_file_pathes[0]
    latest_date = get_file_timestamp(log_file_pathes[0])
    for file_path in log_file_pathes:
        timestamp = get_file_timestamp(file_path)
        if timestamp < latest_date:
            latest_log = file_path
            latest_date = timestamp

    return latest_log


def calculate_report_file_path(file_path: str) -> str:
    """ Function for calculation report file path based on input log_file_path """
    
    log_timestamp = get_file_timestamp(file_path)
    datetime_obj = datetime.datetime.strptime(log_timestamp, '%Y%m%d')
    report_timestamp = datetime_obj.strftime('%Y.%m.%d')
    report_filename = 'report-' + str(report_timestamp) + '.html'
    return os.path.join(config['report_dir'], report_filename)


def check_report_file_already_exists(file_path: str) -> bool:
    """ Check that log parsing job is already done
        If file with report name already exists, returns True"""

    return os.path.exists(file_path)


def decompress_log_file(log_file_path: str) -> str:
    """ Function checks that file is archive
        If so function decompress file 
        and returns new file name without gz extension """

    with gzip.open(log_file_path, 'rb') as input_file:
        new_report_file_path, gz_extension = os.path.splitext(log_file_path)
        with open(new_report_file_path, 'wb') as output_file:
            shutil.copy(input_file, output_file)
        return new_report_file_path
            
            
def get_file_timestamp(filename: str) -> int:
    """ Function parses filename according to known structure and returns timestamp """

    chunks = filename.split('-')
    if 'gz' in chunks[-1]:
        next_chunks = chunks[-1].split('.')
        return next_chunks[0]
    else:
        return chunks[-1]


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

log_file_path = find_last_log_file(config)
report_file_path = calculate_report_file_path(log_file_path)
if check_report_file_already_exists(report_file_path):
    #TODO
    pass

if log_file_path.endswith('gz'):
    log_file_path = decompress_log_file()

log_analyzer = LogAnalyser(config, log_file_path, report_file_path)
log_analyzer.analyze_log()

