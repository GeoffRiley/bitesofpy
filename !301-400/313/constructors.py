import re


class DomainException(Exception):
    """Raised when an invalid is created."""


class Domain:

    def __init__(self, name):
        # validate a current domain (r'.*\.[a-z]{2,3}$' is fine)
        # if not valid, raise a DomainException
        if not re.match(r'.*\.[a-z]{2,3}$', name, re.IGNORECASE):
            raise DomainException(f'Bad domain {name}')
        self.name = name

    # next add a __str__ method and write 2 class methods
    # called parse_from_url and parse_from_email to construct domains
    # from an URL and email respectively
    def __str__(self):
        return self.name

    @classmethod
    def parse_url(cls, url):
        # Comment in template incorrectly suggests this should be parse_from_url
        return cls(re.sub(r'^https?://([^/]+)(?:/.*)?$', r'\1', url))

    @classmethod
    def parse_email(cls, email):
        # Comment in template incorrectly suggests this should be parse_from_email
        return cls(re.sub(r'^.*@(.+)$', r'\1', email))
