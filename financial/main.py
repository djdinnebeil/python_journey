import sqlite3
import pandas as pd
import numpy as np
from db_singleton import DatabaseConnection
from company_class import CompanyFactory

# Define the Bollinger Band width as a global variable
bollinger_width = 2

# Define the Window Size for Movine Average
window_size = 20

conn = DatabaseConnection().get_connection()

# Get company by ticker or ID
# company = CompanyFactory.get_company('GOOGL', conn)
# if company:
#     company.load_time_series(conn)
#     company.calculate_bollinger_bands()
#     company.assign_grade()
#     company.display()
#
# print('--------')
#
# company = CompanyFactory.get_company('AAPL', conn)
# if company:
#     company.load_time_series(conn)
#     company.calculate_bollinger_bands()
#     company.assign_grade()
#     company.display()


# Get domestic company by ticker
# try:
#     domestic_company = CompanyFactory.get_company('AAPL', conn)
#     if domestic_company:
#         domestic_company.load_time_series(conn)
#         domestic_company.calculate_bollinger_bands()
#         domestic_company.display()
#     else:
#         print("Domestic company not found")
# except Exception as e:
#     print(f"Error processing domestic company: {e}")

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
#
# #Print the name and type of each company you just created
# print(f"The name of the domestic company is: {domestic_company.name}")
# print(f"{domestic_company.name} is a {domestic_company.company_type} company.")
# print(f"The name of the foreign company is: {foreign_company.name}")
# print(f"{foreign_company.name} is a {foreign_company.company_type} company.")

DatabaseConnection.close_connection()