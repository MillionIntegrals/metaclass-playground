import json


class Field:
    """ Base class for all Fields. Every field needs an initial value """

    def __init__(self, initial_value=None):
        self.initial_value = initial_value

    def validate(self, value):
        """ Check if this is a valid value for this field """
        return True


class StringField(Field):
    """ A string field. Optionally validates length of a string """

    def __init__(self, initial_value=None, maximum_length=None):
        super().__init__(initial_value)

        self.maximum_length = maximum_length

    def validate(self, value):
        """ Check if this is a valid value for this field """
        if super().validate(value):
            return (value is None) or (isinstance(value, str) and self._validate_length(value))
        else:
            return False

    def _validate_length(self, value):
        """ Check if string has correct length """
        return (self.maximum_length is None) or (len(value) <= self.maximum_length)


class IntField(Field):
    """ An integer field. Optionally validates if integer is be"""

    def __init__(self, initial_value=None, maximum_value=None):
        super().__init__(initial_value)

        self.maximum_value = maximum_value

    def validate(self, value):
        """ Check if this is a valid value for this field """
        if super().validate(value):
            return (value is None) or (isinstance(value, int) and self._validate_value(value))
        else:
            return False

    def _validate_value(self, value):
        """ Check if integer falls in desired range """
        return (self.maximum_value is None) or (value <= self.maximum_value)


class ORMMeta(type):
    """ Metaclass of our own ORM """
    def __new__(self, name, bases, namespace):
        fields = {name: field for name, field in namespace.items() if isinstance(field, Field)}

        new_namespace = namespace.copy()

        # Remove fields from class variables
        for name in fields.keys():
            del new_namespace[name]

        new_namespace['_fields'] = fields

        return super().__new__(self, name, bases, new_namespace)


class ORMBase(metaclass=ORMMeta):
    """ User interface for the base class """

    def __init__(self, json_input=None):
        for name, field in self._fields.items():
            setattr(self, name, field.initial_value)

        # If there is a JSON supplied, we'll parse it
        if json_input is not None:
            json_value = json.loads(json_input)

            if not isinstance(json_value, dict):
                raise RuntimeError("Supplied JSON must be a dictionary")

            for key, value in json_value.items():
                setattr(self, key, value)

    def __setattr__(self, key, value):
        """ Magic method setter """
        if key in self._fields:
            if self._fields[key].validate(value):
                super().__setattr__(key, value)
            else:
                raise AttributeError('Invalid value "{}" for field "{}"'.format(value, key))
        else:
            raise AttributeError('Unknown field "{}"'.format(key))

    def to_json(self):
        """ Convert given object to JSON """
        new_dictionary = {}

        for name in self._fields.keys():
            new_dictionary[name] = getattr(self, name)

        return json.dumps(new_dictionary)


class User(ORMBase):
    """ A user in our system """
    id = IntField(initial_value=0, maximum_value=2**32)
    name = StringField(maximum_length=200)
    surname = StringField(maximum_length=200)
    height = IntField(maximum_value=300)
    year_born = IntField(maximum_value=2017)


u = User()
u.name = "Guido"
u.surname = "Van Rossum"

print("User ID={}".format(u.id))
print("User JSON={}".format(u.to_json()))

w = User('{"id": 5, "name": "John", "surname": "Smith", "height": 185, "year_born": 1989}')

print("User ID={}".format(w.id))
print("User NAME={}".format(w.name))


try:
    u.favourite_joke = "Knock, knock"
except AttributeError as e:
    print(e)

try:
    u.height = 500
except AttributeError as e:
    print(e)

try:
    User('{"year_born": 3000}')
except AttributeError as e:
    print(e)
