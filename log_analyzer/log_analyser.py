from statistics import mean, median
import json
import logging
import gzip
logger = logging.getLogger(__name__)


class LogAnalyser:
    def __init__(self, config, log_path, report_path):
        self._report_size = config['report_size']
        self._log_file_path = log_path
        self._report_file_path = report_path
        self._urls_stat = dict()
        self._report_table = list()
        self._total_request_count = 0
        self._total_request_time = 0
        self._max_error_count = config['max_error_count'] if 'max_error_count' in config else None
        self._total_error_count = 0

    def analyse_log(self) -> bool:
        """ Public function that does main job about parsing last ngnix log """

        self._process_log_file()
        self._calculate_url_statistics()
        self._render_report_template()

    def _process_log_file(self) -> None:
        """ Processing log file line by line """

        opener = gzip.open if self._log_file_path.endswith('gz') else open
        with opener(self._log_file_path, encoding='utf-8') as file:
            for line in file:
                result, url, req_time = self._parse_log_line(line)

                if result:
                    if url not in self._urls_stat:
                        self._urls_stat[url] = list()

                    self._urls_stat[url].append(req_time)
                    self._total_request_count += 1
                    self._total_request_time += req_time
                else:
                    self._total_error_count += 1
                    if self._max_error_count and self._total_error_count > self._max_error_count:
                        raise Exception('Failed to parse log: max error count reached. Stop working...')

    def _parse_log_line(self, line: str) -> (bool, str, float):
        """ Function parses log line, validate result
            Returns:
                (bool) parsing and validation result,
                (str) url, if result is ok, None if not
                (float) req_time, if result is ok, None if not """

        chunks = line.split()
        url = chunks[6]
        req_time = chunks[-1]
        if self._validate_log_parsing(url, req_time):
            return True, url, float(req_time)
        else:
            return False, None, None

    def _calculate_url_statistics(self) -> None:
        """ Function calculates all required fields based on log parsing results """

        url_stat_sorted = sorted(self._urls_stat.items(), key=lambda item: sum(item[1]), reverse=True)
        url_stat_sorted_limited = url_stat_sorted[:self._report_size]
        for url_stat in url_stat_sorted_limited:
            row = dict()
            row['url'] = url_stat[0]
            url_req_times = url_stat[1]
            row['count'] = len(url_req_times)
            formatter = '{0:.3f}'
            row['count_perc'] = formatter.format(row['count'] / self._total_request_count * 100).rstrip('0')
            row['time_sum'] = formatter.format(sum(url_req_times)).rstrip('0')
            row['time_perc'] = formatter.format(float(row['time_sum']) / self._total_request_time * 100).rstrip('0')
            row['time_avg'] = formatter.format(mean(url_req_times)).rstrip('0')
            row['time_max'] = formatter.format(max(url_req_times)).rstrip('0')
            row['time_med'] = formatter.format(median(url_req_times)).rstrip('0')
            self._report_table.append(row)

    def _render_report_template(self) -> None:
        """ Function for saving results of log parsing in report """

        table_json = json.dumps(self._report_table)
        with open('report.html') as report_template:
            contents = report_template.read()
            actual_report = contents.replace('$table_json', table_json)
            with open(self._report_file_path, 'w', encoding='utf-8') as report:
                report.write(actual_report)

    @staticmethod
    def _validate_log_parsing(url: str, req_time: str):
        """ Function checks results of log parsing: url and req_time
            url should be string with / (very simple, but can be changed any time)
            req_time should be possible to convert to float """

        if '/' not in url:
            logger.debug(f'Input data problems: {url} is not considered as url')
            return False
        try:
            float(req_time)
        except ValueError:
            logger.debug(f'Input data problems: {req_time} couldn\'t be converted to float')
            return False

        return True


