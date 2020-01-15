import copy
import configparser


class LogAnalyserConfigurator:
    """ Class to calculate Log Analyzer config """

    def __init__(self, default_config: dict, config_file: str) -> None:
        self._default_config = default_config
        self._config_file = config_file

    def get_config(self) -> dict:
        """ Public function to return actual config
            Combine default config and params from file
            Returns dict with actual config """

        params_from_file = self._parse_params()
        config = copy.copy(self._default_config)
        config.update(params_from_file)
        return config

    def _parse_params(self) -> dict:
        """ Function to parse params from self._config_file
            Returns dict with params """

        try:
            config_string = self._get_config_string()
            parser = configparser.ConfigParser()
            parser.read_string(config_string)
            return dict(parser.items('Default'))
        except Exception:
            raise

    def _get_config_string(self) -> str:
        """ Workaround for configparser library : this function adds [Default] section to self._config_file contents
            Return string """

        with open(self._config_file, encoding='utf-8') as file:
            contents = file.read()
            return '[Default]\n' + contents
