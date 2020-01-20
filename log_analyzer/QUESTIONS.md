Вопросы:
1.  У меня возник вопрос, как модули программы должны соощать об ошибках в процессе выполнения вызывающим их модулям или внутри самих себя.

*   Например, превышен порог ошибок парсинга логов.
    Читаю 'Clean code' и они пишут: не пользуйтесь Exceptions для того, чтобы программировать бизнес-логику.
    Вопрос: реализацию порога ошибок и выхода, если он превышен, можно отнести к бизнес логике или нет?
    Я считаю, что это не совсем бизнес-логика, а обработка того, чего в принципе не должно случиться, поэтому сгенерила Exception

*   не совсем понимаю, как правильно использовать Exceptions

    Хочу разобраться, как лучше писать для того, чтобы было понятнее разбираться и поддерживать код.
    В том же 'Clean code' написано, что Exception - это когда нужно перестать использовать выполнять программу, 
    Что лучше должна возвращать функция-валидатор? True/False или Exception? 

    Текущий вариант:
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
        
    Предыдущий вариант (с генерацией Exception). В коде, вызывающем эту функцию я обрабатываю результат с помощью try.
    Мне не понравился такой подход, потому что этот блок кода (с созданием try контекста) должен быть выполнен столько раз, сколько строк в логе.
    Является ли создание контекста try трудоёмким для питона? стоит ли переживать по этому поводу?

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

        
*   правильно ли писать try с большим количеством операций внутри как у меня в entrypoint?
    Я это делаю для перехвата всевозможных Exceptions для того, чтобы они попали в лог

2.  В тексте задания написано "функцию, которая будет парсить лог желательно сделать генератором"
    Понимаю, что это необязательно, но зачем такая рекомендация? Ведь проход по файлу лога - это операция
    итерирования, т.е. много памяти не должна занимать.

3.  в задании написано:
    "найти самый свежий лог можно за один проход по файлам, без использования glob, сортировки и т.п.№
    Почему использовать glob плохо? я тоже нахожу нужный лог за 1 проход с помощью него.