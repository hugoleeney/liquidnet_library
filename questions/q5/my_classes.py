class Foo:

    def speak(self):
        return "foo"

    def bark(self):
        return "foo"

    def gross(self):
        super(Foo, self).tweet()
        return "bar"

    def eugh(self):
        super(Bar, self).tweet()
        return "bar"

class Bar:

    def speak(self):
        return "bar"

    def bark(self):
        return "bar"

    def tweet(self):
        return "bar"

    def gross(self):
        super(Bar)
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


print(Test.mro())
t = Test()

for i in range(10):
    assert t.speak() == "test"
    assert t.bark() == "foo"
    assert t.tweet() == "bar"
    assert t.gross() == "bar"

    exception_caught = False
    try:
        t.eugh()
    except Exception as e:
        exception_caught = True
    assert exception_caught
