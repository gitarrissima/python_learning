from statistics import mean, median
import json


class LogAnalyser:
    def __init__(self, config, log_path, report_path):
        self._config = config
        self._log_file_path = log_path
        self._report_file_path = report_path
        self._urls_stat = dict()
        self._report_table = list()
        self._total_request_count = 0
        self._total_request_time = 0

    def analyze_log(self):
        """ Public function that does main job about parsing last ngnix log"""

        self._parse_log()
        self._calculate_url_statistics()
        self._render_report_template()

    def _parse_log(self) -> None:
        """ Log parsing itself """

        with open(self._log_file_path, encoding='utf-8') as file:
            for line in file:
                chunks = line.split()
                url = chunks[6]
                req_time = float(chunks[-1])
                if self._validate_log_parsing():
                    # TODO
                    pass

                if url not in self._urls_stat:
                    self._urls_stat[url] = list()

                self._total_request_count += 1
                self._total_request_time += req_time
                self._urls_stat[url].append(req_time)

    def _calculate_url_statistics(self):
        """ Function calculates all required fields based on log parsing results """

        url_stat_sorted = sorted(self._urls_stat.items(), key=lambda item: sum(item[1]), reverse=True)
        url_stat_sorted_limited = url_stat_sorted[:self._config['report_size']]
        for url_stat in url_stat_sorted_limited:
            row = dict()
            row['url'] = url_stat[0]
            url_req_times = url_stat[1]
            row['count'] = len(url_req_times)
            row['count_perc'] = "{0:.4f}".format(row['count'] / self._total_request_count)
            row['time_sum'] = sum(url_req_times)
            row['time_perc'] = "{0:.4f}".format(row['time_sum'] / self._total_request_time)
            row['time_avg'] = mean(url_req_times)
            row['time_max'] = max(url_req_times)
            row['time_med'] = median(url_req_times)
            self._report_table.append(row)

    def _validate_log_parsing(self):
        #TODO
        return True

    def _render_report_template(self) -> None:
        """ Function for saving results of log parsing in report """

        table_json = json.dumps(self._report_table)
        with open('report.html') as report_template:
            contents = report_template.read()
            actual_report = contents.replace('$table_json', table_json)
            with open(self._report_file_path, 'w', encoding='utf-8') as report:
                report.write(actual_report)


