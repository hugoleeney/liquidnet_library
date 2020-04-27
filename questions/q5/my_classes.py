class Foo:

    def speak(self):
        return "foo"

    def bark(self):
        return "foo"



class Bar:

    def speak(self):
        return "bar"

    def bark(self):
        return "bar"

    def tweet(self):
        return "bar"


class Zaz:

    def speak(self):
        raise Exception()

    def bark(self):
        raise Exception()

    def tweet(self):
        raise Exception()


class Test(Foo, Bar, Zaz):

    def speak(self):
        return 'test'


t = Test()

for i in range(10):
    assert t.speak() == "test"
    assert t.bark() == "foo"
    assert t.tweet() == "bar"
