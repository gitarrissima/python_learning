import glob
import os
import datetime
import logging
logger = logging.getLogger(__name__)


class LogAnalyserHelper:
    def __init__(self, config: dict):
        self._log_dir = config['log_dir']
        self._report_dir = config['report_dir']
        self._log_file_path = str()
        self._report_file_path = str()

    def find_last_log_file(self) -> str:
        """ Function searches for latest log file in config.log_dir directory
            Returns name of file if it exists """

        log_filename_template = os.path.join(self._log_dir, "nginx-access-ui.log-*")
        log_file_pathes = glob.glob(log_filename_template)
        if len(log_file_pathes) == 0:
            return None
        latest_log = log_file_pathes[0]
        latest_date = self._get_file_timestamp(log_file_pathes[0])
        for file_path in log_file_pathes:
            timestamp = self._get_file_timestamp(file_path)
            if timestamp > latest_date:
                latest_log = file_path
                latest_date = timestamp

        self._log_file_path = latest_log
        return latest_log

    def calculate_report_file_path(self) -> str:
        """ Function for calculation report file path based on log_file_path """

        log_timestamp = self._get_file_timestamp(self._log_file_path)
        datetime_obj = datetime.datetime.strptime(log_timestamp, '%Y%m%d')
        report_timestamp = datetime_obj.strftime('%Y.%m.%d')
        report_filename = "report-{}.html".format(str(report_timestamp))
        self._report_file_path = os.path.join(self._report_dir, report_filename)
        return self._report_file_path

    def check_report_file_already_exists(self) -> bool:
        """ Check that log parsing job is already done
            If file with report name already exists, returns True"""

        return os.path.exists(self._report_file_path)

    @staticmethod
    def _get_file_timestamp(filename: str) -> int:
        """ Function parses filename according to known structure and returns timestamp """

        chunks = filename.split('-')
        if 'gz' in chunks[-1]:
            next_chunks = chunks[-1].split('.')
            return next_chunks[0]
        else:
            return chunks[-1]
