
class Person:

    def __init__(self, name, age, sex, holiday, style, text_length, interests):
        self.__name = name
        self.__age = age
        self.__sex = sex
        self.__holiday = holiday
        self.__style = style
        self.__text_length = text_length
        self.__interests = interests

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age = age

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, sex):
        self.__sex = sex

    @property
    def holiday(self):
        return self.__holiday

    @holiday.setter
    def holiday(self, holiday):
        self.__holiday = holiday

    @property
    def style(self):
        return self.__style

    @style.setter
    def style(self, style):
        self.__style = style

    @property
    def interests(self):
        return self.__interests

    @interests.setter
    def interests(self, interests):
        self.__interests = interests

    @property
    def text_length(self):
        return self.__text_length

    @text_length.setter
    def text_length(self, text_length):
        self.__text_length = text_length

    def __del__(self):
        pass
