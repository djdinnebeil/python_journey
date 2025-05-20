# company\types.py
from enum import Enum

_company_type_registry = {}

class CompanyType(str, Enum):
    DOMESTIC = 'domestic'
    FOREIGN = 'foreign'
    CRYPTO = 'crypto'

    def __str__(self):
        return self.value

    @classmethod
    def register(cls, enum_value):
        def decorator(company_class):
            _company_type_registry[enum_value] = company_class
            return company_class
        return decorator

    @classmethod
    def resolve_class(cls, enum_value):
        return _company_type_registry.get(enum_value)

    @classmethod
    def get_class(cls, raw_value):
        try:
            enum_member = cls(raw_value)
            return cls.resolve_class(enum_member)
        except ValueError:
            return None
