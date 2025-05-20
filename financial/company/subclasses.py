# company\subclasses.py
from .base import Company
from .types import CompanyType

@CompanyType.register(CompanyType.DOMESTIC)
class DomesticCompany(Company):
    def __init__(self, company_id, ticker, name):
        super().__init__(company_id, ticker, name)
        self.company_type = CompanyType.DOMESTIC

    def pre_pipeline(self):
        print('domestic pipeline overriding')

    def get_pipeline(self):
        print('domestic pipeline')

@CompanyType.register(CompanyType.FOREIGN)
class ForeignCompany(Company):
    def __init__(self, company_id, ticker, name):
        super().__init__(company_id, ticker, name)
        self.company_type = CompanyType.FOREIGN

    def get_pipeline(self):
        print('foreign pipeline')

@CompanyType.register(CompanyType.CRYPTO)
class CryptoCompany(Company):
    def __init__(self, company_id, ticker, name):
        super().__init__(company_id, ticker, name)
        self.company_type = CompanyType.CRYPTO

    def get_pipeline(self):
        print('crypto pipeline')
