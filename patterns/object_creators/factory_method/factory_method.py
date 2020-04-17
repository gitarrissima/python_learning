import configparser


class Character:

    def __init__(self):
        pass

    def method_1(self):
        pass

    def method_2(self):
        pass


class A(Character):

    def __init__(self):
        pass

    def method_1(self):
        print('Class A method_1 output')

    def method_2(self):
        print('Class A method_2 output')


class B(Character):

    def __init__(self):
        pass

    def method_1(self):
        print('Class B method_1 output')

    def method_2(self):
        print('Class B method_2 output')


class Article:

    def __init__(self):
        pass

    def write(self):
        c = self.create_character()
        c.method_1()
        c.method_2()

    def create_character(self):
        pass


class AArticle(Article):

    def create_character(self):
        return A()


class BArticle(Article):

    def create_character(self):
        return B()


class Application:
    article = None

    def __init__(self):
        character = None

        with open('config.py', encoding='utf-8') as f:
            contents = f.read()
            parser = configparser.ConfigParser()
            parser.read_string(contents)
            if parser.has_option('Default', 'character'):
                character = parser.get('Default', 'character')

        if character == 'A':
            self.article = AArticle()
        else:
            self.article = BArticle()


if __name__ == '__main__':
    app = Application()
    app.article.write()

