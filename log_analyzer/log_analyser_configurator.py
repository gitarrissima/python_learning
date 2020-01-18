import copy
import configparser
import logging
logger = logging.getLogger(__name__)

class LogAnalyserConfigurator:
    """ Class to calculate Log Analyzer config """

    def __init__(self, default_config: dict, config_file: str) -> None:
        self._default_config = default_config
        self._config_file = config_file

    def get_config(self) -> dict:
        """ Public function to return actual config
            Combine default config and params from file
            Returns dict with actual config """

        try:
            params_from_file = self._parse_params()
            config = copy.copy(self._default_config)
            config.update(params_from_file)
            return config
        except Exception as e:
            logger.exception(e)
            raise

    def _parse_params(self) -> dict:
        """ Function to parse params from self._config_file
            Returns dict with params """

        try:
            config_string = self._get_config_string()
            parser = configparser.ConfigParser()
            parser.read_string(config_string)
            config = dict()
            if parser.has_option('Default', 'log_dir'):
                config['log_dir'] = parser.get('Default', 'log_dir')
            if parser.has_option('Default', 'report_dir'):
                config['report_dir'] = parser.get('Default', 'report_dir')
            if parser.has_option('Default', 'report_size'):
                config['report_size'] = parser.getint('Default', 'report_size')
            if parser.has_option('Default', 'max_error_count'):
                config['max_error_count'] = parser.getint('Default', 'max_error_count')
            return config
        except Exception:
            raise

    def _get_config_string(self) -> str:
        """ Workaround for configparser library : this function adds [Default] section to self._config_file contents
            Return string """

        with open(self._config_file, encoding='utf-8') as file:
            contents = file.read()
            return '[Default]\n' + contents
