[![Build Status](https://travis-ci.org/biosustain/potion-client.svg?branch=master)](https://travis-ci.org/biosustain/potion-client)
[![Coverage Status](https://coveralls.io/repos/biosustain/potion-client/badge.svg?branch=master)](https://coveralls.io/r/biosustain/potion-client?branch=master)

# Potion client

A client for REST APIs documented using JSON-schema in general, and `Flask-Potion` in particular.

## Example


    c = Client('http://localhost/api/schema')
    
    Project = c.Project
    Project.instances
    Project.instances.where(key=value)
    
    p = Project(1)
    p.name = "super project"
    p.save()
    
    User = c.User
    u = User()
    u.name = "Name"
    u.projects = [p]
    u.save()

    query = Project.instances.where(user=u)


## Extensions Example
```python

class ProjectExtension(object):
    _extends = ["Project"]

    def email_managers(self):
        for mangers in self.managers:
            # send an email using smtplib etc. etc

extensions = [ProjectExtension]

c = Client('http://localhost/api/schema', extensions=extensions)

Project = c.Project
project = Project.instances()[0]

# the email managers function has been added to the project resource
project.email_managers()

query = Project.instances.where(user=u)
```
    
## Dependencies

- [requests](http://docs.python-requests.org/en/latest/) for HTTP requests
- [jsonschema](http://python-jsonschema.readthedocs.org/en/latest/)
