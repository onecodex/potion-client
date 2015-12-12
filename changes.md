# PR Changes Documentation

## 1. Refactor for python 2 compatibility
- The first major thing I did was refactor the code to be compatible with python 2. This was a mostly autoated process using the python package `3to2`. The majority of the changes where the removal of method type statements.

I did have to solve a few issues manually:
- factory method in Routes()
    - In the factory method, the newly created resource class had its `__doc__` variable set, however this throws an error in python 2.
    - It appears the behavior is a bug, which was fixed in python 3 as per this report: [bug](http://bugs.python.org/issue12773). I found that the bug was apperentally not backported to python 2 [here](http://www.gossamer-threads.com/lists/python/dev/962536)
- Unicode strings
    In python 3 all strings are unicode, not the case in python 2. There were a few cases where responses from the api were being treated as unicode.
- Timezone
    In python 3, the datetime module had a timezone functionality added to it. Allowing for things like this:
    `date.fromtimestamp(0, timezone.utc)`
    We have to use `pytz` to do this in python 2
    `date.fromtimestamp(0, pytz.utc)`

## 2. Add extension functionality
- The goal here was to allow for client side only additions to the resources of the api. Our running example for this was: Imagine some resource called File, which has a `url` attribute that points to an aws s3 file. A client lib based on the api would want to provide this functionality: `file.download(file_name)` which will download the file based on the url attribute. We introduce an additional parameter to the client construtor called extensions, which should contain an array of Mixin/Extension classes.

- The extension classes should look something like:
```python
class FooExtension(object):
    _extends = ["Foo"]  # required array specifying which resource to apply this ext to

    def download_file(self):
        # dl file here
```

- The classes must have _extends defined, and the values in it must match an api resource name.
We can have an extension apply to multiple different resource by simply adding them to the array.

- At the moment there is no checking whether an extension makes use of resource attributes that may not exist. Since this functionality is focused on people using potion client as a basis for their own client libs, we feel like such checking may not be needed at this time.

- We have also added an additional exception (which arises when an extension class is passed to the constructor without an `_extends` array)

- `test_extensions.py` provides a few test cases to ensure the new functionality is working.