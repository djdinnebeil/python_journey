import sqlite3
import pandas as pd
from enum import Enum

# -----------------------------------
# EXTERNAL REGISTRY FOR ENUM-CLASS MAPPING
# -----------------------------------
_company_type_registry = {}

# -----------------------------------
# ENUM FOR COMPANY TYPES
# -----------------------------------
class CompanyType(str, Enum):
    DOMESTIC = 'domestic'
    FOREIGN = 'foreign'

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


# -----------------------------------
# BASE COMPANY CLASS
# -----------------------------------
class Company:
    def __init__(self, company_id, ticker, name):
        self.company_id = company_id
        self.ticker = ticker
        self.name = name
        self.time_series = None
        self.high_bollinger = None
        self.low_bollinger = None
        self.moving_average = None
        self.grade = None

    def load_time_series(self, conn):
        query = '''
        SELECT date, value
        FROM TimeSeries
        WHERE company_id = ?
        ORDER BY date
        '''
        self.time_series = pd.read_sql_query(query, conn, params=(self.company_id,))
        self.time_series['date'] = pd.to_datetime(self.time_series['date'])

    def calculate_bollinger_bands(self, window_size=20, bollinger_width=2):
        rolling_mean = self.time_series['value'].rolling(window_size).mean()
        rolling_std = self.time_series['value'].rolling(window_size).std()
        self.moving_average = rolling_mean
        self.high_bollinger = rolling_mean + (rolling_std * bollinger_width)
        self.low_bollinger = rolling_mean - (rolling_std * bollinger_width)

    def assign_grade(self):
        latest_value = self.time_series['value'].iloc[-1]
        if latest_value > self.high_bollinger.iloc[-1]:
            self.grade = 'A'
        elif latest_value < self.low_bollinger.iloc[-1]:
            self.grade = 'C'
        else:
            self.grade = 'B'

    def display(self):
        print(f'Company: {self.name} ({self.ticker})')
        print(f'Grade: {self.grade}')
        print('Time Series Tail:')
        print(self.time_series.tail())


# -----------------------------------
# SUBCLASSES FOR SPECIFIC TYPES
# -----------------------------------
@CompanyType.register(CompanyType.DOMESTIC)
class DomesticCompany(Company):
    def __init__(self, company_id, ticker, name):
        super().__init__(company_id, ticker, name)
        self.company_type = CompanyType.DOMESTIC

@CompanyType.register(CompanyType.FOREIGN)
class ForeignCompany(Company):
    def __init__(self, company_id, ticker, name):
        super().__init__(company_id, ticker, name)
        self.company_type = CompanyType.FOREIGN


# -----------------------------------
# FACTORY CLASS
# -----------------------------------
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
