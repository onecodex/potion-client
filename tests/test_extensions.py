from potion_client import Client
from potion_client_testing import MockAPITestCase
from httmock import HTTMock
from datetime import datetime
import pytz
from potion_client.exceptions import InvalidExtensionException


class ExtensionsTestCase(MockAPITestCase):

    def _create_foo(self, attr1="value1", attr2="value2"):
        foo = self.potion_client.Foo()
        foo.attr1 = attr1
        foo.attr2 = attr2
        foo.attr3 = "attr3"
        foo.date = self.time
        foo.save()
        return foo

    def _create_foo_with_mapped_biz(self, attr1="value1"):
        foo = self.potion_client.FooWithMappedBiz()
        foo.attr1 = attr1
        foo.date = self.time
        foo.save()
        return foo

    def _create_bar(self, attr1=5, foo=None):
        bar = self.potion_client.Bar()
        bar.attr1 = attr1
        bar.foo = foo
        bar.save()
        return bar

    def _create_baz(self, attr1=1.0, attr2=None, foo=None):
        baz = self.potion_client.Baz(attr1=attr1, foo=foo, attr2=attr2)
        baz.save()
        return baz

    def _create_biz(self, attr1="value1", attr2=1.0):
        biz = self.potion_client.Biz(attr1=attr1, attr2=attr2)
        biz.save()
        return biz

    def setUp(self):
        self.time = datetime.fromtimestamp(0, pytz.utc)
        MockAPITestCase.setUp(self)

    def test_simple_foo_extension(self):

        class FooExtension(object):
            _extends = ["Foo"]

            def return_foo(self):
                return "foo"

        extensions = [FooExtension]

        with HTTMock(self.get_mock, self.post_mock):
            self.potion_client = Client(extensions=extensions)
            foo = self._create_foo()
            self.assertEqual(foo.return_foo(), "foo")

    def test_relation_extensions(self):

        class FooExtension(object):
            _extends = ["Foo"]

            def return_foo(self):
                return "foo"

        class BarExtension(object):
            
            _extends = ["Bar"]
            extended_meassge = "I have been extended!"

            def return_foo_from_relation(self):
                return self.foo.return_foo()

        extensions = [FooExtension, BarExtension]

        with HTTMock(self.get_mock, self.post_mock):
            self.potion_client = Client(extensions=extensions)
            
            self._create_foo()
            foo = self.potion_client.Foo.instances()[0]
            
            self._create_bar(foo=foo)
            bar = self.potion_client.Bar.instances()[0]

            self.assertEqual(foo.return_foo(), "foo")
            self.assertEqual(bar.return_foo_from_relation(), "foo")
            self.assertEqual(bar.extended_meassge, "I have been extended!")

    def test_two_foo_extensions(self):
        
        class FooExtension(object):
            _extends = ["Foo"]

            def return_foo(self):
                return "foo"

        class AnoterFooExtension(object):
            _extends = ["Foo"]

            def return_bar(self):
                return "bar"

        extensions = [FooExtension, AnoterFooExtension]

        with HTTMock(self.post_mock, self.get_mock):
            self.potion_client = Client(extensions=extensions)
            foo = self._create_foo()
            self.assertEqual(foo.return_foo(), "foo")
            self.assertEqual(foo.return_bar(), "bar")

    def test_extending_foo_and_bar(self):

        class FooBarExtension(object):
            _extends = ["Foo", "Bar"]

            def return_foobar(self):
                return "fooBar"

        extensions = [FooBarExtension]

        with HTTMock(self.post_mock, self.get_mock):
            self.potion_client = Client(extensions=extensions)
            
            self._create_foo()
            foo = self.potion_client.Foo.instances()[0]
            
            self._create_bar(foo=foo)
            bar = self.potion_client.Bar.instances()[0]
            
            self.assertEqual(foo.return_foobar(), "fooBar")
            self.assertEqual(bar.return_foobar(), "fooBar")

    def test_invalid_extension_error(self):

        class InvalidFooExtension(object):

            def return_foobar(self):
                return "fooBar"

        extensions = [InvalidFooExtension]
        with HTTMock(self.post_mock, self.get_mock):
            self.failUnlessRaises(InvalidExtensionException, Client, extensions=extensions)