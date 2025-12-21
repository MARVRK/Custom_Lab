class Age:
    def __init__(self, age):
        self.age = age
        if 1 > self.age < 100:
            raise ValueError("Wrong Age range")


class Email:
    def __init__(self, email):
        self.email = email
        if "@" not in self.email:
            raise ValueError("Wrong Email format")

class Meta(type):
    __fields__ = {}
    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        new_cls.__fields__ = new_cls.__annotations__
        return new_cls

class BasicMode(metaclass=Meta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.__class__.__fields__:
                raise ValueError("Type was not included in that class")
            expected_type = self.__class__.__fields__[key]
            if not isinstance(value, expected_type):
                raise ValueError("Wrong type")
            setattr(self, key, value)


class TestModel(BasicMode):
    name: str
    id: int
    age: Age
    email: Email


cp = TestModel(name="Sally", id=1, email=Email("some@some.pl"), age=Age(2))
print(cp.__dict__)
