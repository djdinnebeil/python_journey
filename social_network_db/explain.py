from sqlalchemy import create_engine, inspect

engine = create_engine('sqlite:///social_network.db')
inspector = inspect(engine)

for table_name in inspector.get_table_names():
    print(f'\nTable: {table_name}')
    for column in inspector.get_columns(table_name):
        print(f"  {column['name']} ({column['type']})")
