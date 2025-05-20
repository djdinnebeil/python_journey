# company\base.py
import sqlite3
import pandas as pd
from abc import ABC, abstractmethod

class Company(ABC):
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

    def run_analysis_pipeline(self, conn):
        self.pre_pipeline()
        self.load_time_series(conn)
        self.calculate_bollinger_bands()
        self.assign_grade()
        self.display()
        self.get_pipeline()

    @abstractmethod
    def get_pipeline(self):
        pass

    def pre_pipeline(self):
        print('domestic overrides this')