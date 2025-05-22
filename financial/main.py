# main.py
from db.connection import DatabaseConnection
from company.factory import CompanyFactory
from company.base import Company

# Define the Bollinger Band width as a global variable
bollinger_width = 2

# Define the Window Size for Moving Average
window_size = 20

conn = DatabaseConnection().get_connection()

# Get company by ticker or ID
company = CompanyFactory.get_company('GOOGL', conn)
if company:
    company.load_time_series(conn)
    company.calculate_bollinger_bands()
    company.assign_grade()
    company.display()

print('--------')

company = CompanyFactory.get_company('AAPL', conn)
if company:
    company.load_time_series(conn)
    company.calculate_bollinger_bands()
    company.assign_grade()
    company.display()


# Get domestic company by ticker
try:
    domestic_company = CompanyFactory.get_company('AAPL', conn)
    if domestic_company:
        domestic_company.load_time_series(conn)
        domestic_company.calculate_bollinger_bands()
        domestic_company.display()
    else:
        print("Domestic company not found")
except Exception as e:
    print(f"Error processing domestic company: {e}")

# # Get foreign company by ID
try:
    foreign_company = CompanyFactory.get_company(1001, conn)
    if foreign_company:
        foreign_company.load_time_series(conn)
        foreign_company.calculate_bollinger_bands()
        foreign_company.display()
    else:
        print("Foreign company not found")
except Exception as e:
    print(f"Error processing foreign company: {e}")

#Print the name and type of each company you just created
print(f"The name of the domestic company is: {domestic_company.name}")
print(f"{domestic_company.name} is a {domestic_company.company_type} company.")
print(f"The name of the foreign company is: {foreign_company.name}")
print(f"{foreign_company.name} is a {foreign_company.company_type} company.")

class GradingStrategy:
    def assign_grade(self, company):
        raise NotImplementedError

class BollingerBandGradingStrategy(GradingStrategy):
    def assign_grade(self, company):
        latest_value = company.time_series['value'].iloc[-1]
        if latest_value > company.high_bollinger.iloc[-1]:
            company.grade = 'A'
        elif latest_value < company.low_bollinger.iloc[-1]:
            company.grade = 'C'
        else:
            company.grade = 'B'

try:
    crypto_company = CompanyFactory.get_company('XBTC', DatabaseConnection.get_connection())
    if crypto_company:
        crypto_company.load_time_series(DatabaseConnection.get_connection())
        crypto_company.calculate_bollinger_bands()
        grading_strategy = BollingerBandGradingStrategy()
        crypto_company.assign_grade()
        crypto_company.display()
    else:
        print("Crypto company not found")
except Exception as e:
    print(f"Error processing crypto company: {e}")
print(f"The name of the crypto company is: {crypto_company.name}")
print(f"{crypto_company.name} is a {crypto_company.company_type} company.")

try:
    domestic_company = CompanyFactory.get_company('MSFT', conn)
    if domestic_company:
        domestic_company.run_analysis_pipeline(conn)
    else:
        print("Domestic company not found")
except Exception as e:
    print(f"Error processing domestic company: {e}")

try:
    foreign_company = CompanyFactory.get_company(1001, conn)
    if foreign_company:
        foreign_company.run_analysis_pipeline(conn)
    else:
        print('Foreign company not found')
except Exception as e:
    print(f'Error processing domestic company: {e}')

DatabaseConnection.close_connection()