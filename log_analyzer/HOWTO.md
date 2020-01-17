Вопросы:
1. У меня возник вопрос, как модули программы должны соощать об ошибках в процессе выполнения вызывающим их модулям или внутри самих себя.

* Например, превышен порог ошибок парсинга логов.
Читаю 'Clean code' и они пишут: не пользуйтесь Exceptions для того, чтобы программировать бизнес-логику.
Вопрос: реализацию порога ошибок и выхода, если он превышен, можно отнести к бизнес логике или нет?
Я считаю, что это не совсем бизнес-логика, а обработка того, чего в принципе не должно случиться, поэтому сгенерила Exception

* не совсем понимаю, как правильно использовать Exceptions
Вот такой пример использования корректен (из log_analyser)?
По сути это валидатор данных:

    @staticmethod
    def _validate_log_parsing(url: str, req_time: str):
        """ Function checks results of log parsing: url and req_time
            url should be string with / (very simple, but can be changed any time)
            req_time should be possible to convert to float """

        if '/' not in url:
            raise Exception(f'Input data problems: {url} is not considered url')
        try:
            float(req_time)
        except ValueError:
            raise

Хочу разобраться, как лучше писать для того, чтобы было понятнее разбираться и поддерживать код.
Или лучше вариант описанный ниже, который был предыдущим?
В том же 'Clean code' написано, что Exception - это когда нужно перестать использовать выполнять программу, 
но в старом ваианта _validate_log_parsing я перехватывала Exception и не останавливаю работу, так как это допустимо до некоторого момента.
А вот когда порог превышен, то кидала Exception, который не перехватываю (но это уже в вызывающей функции).

    def _validate_log_parsing(url: str, req_time: str):
        """ Function checks results of log parsing: url and req_time
            url should be string with / (very simple, but can be changed any time)
            req_time should be possible to convert to float """
        
        if '/' not in url:
            return False
        try:
            float(req_time)
        except ValueError as e:
            logger.info(e)
            return False
        return True
        
* правильно ли писать try с большим количеством операций внутри как у меня в entrypoint?
Я это делаю для перехвата всевозможных Exceptions для того, чтобы они попали в лог