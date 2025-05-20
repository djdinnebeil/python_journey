# company\factory.py
from .types import CompanyType
from . import subclasses

class CompanyFactory:
    @staticmethod
    def get_company(identifier, conn):
        cursor = conn.cursor()
        if isinstance(identifier, str):
            query = 'SELECT id, ticker, name, company_type FROM companies WHERE ticker = ?'
            cursor.execute(query, (identifier,))
        else:
            query = 'SELECT id, ticker, name, company_type FROM companies WHERE id = ?'
            cursor.execute(query, (identifier,))

        row = cursor.fetchone()
        if row:
            company_id, ticker, name, company_type = row
            company_class = CompanyType.get_class(company_type)
            return company_class(company_id, ticker, name)
        return None
