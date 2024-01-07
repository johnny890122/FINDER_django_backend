# https://docs.python.org/3/library/sqlite3.html
import sqlite3
from typing import List, Dict
class Database:
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None
        self.existing_relation = self.__fetch_existing_table()

    def __execute(self, sql: str) -> List:
        return self.cursor.execute(sql)
    
    def __build_connection(func):
        def wrapper(self, *args, **kwargs):
            self.connection = sqlite3.connect('db.sqlite3')
            self.cursor = self.connection.cursor()
            response = func(self, *args, **kwargs)
            self.cursor.close()
            self.connection.close()
            return response
        return wrapper

    @__build_connection
    def __fetch_existing_table(self):
        table_names = self.cursor.execute("SELECT * FROM sqlite_master WHERE type='table';").fetchall()
        return {
            table[1]: {"domain": table[-1]} for table in table_names
        }
    
    @__build_connection
    def clean_database(self):
        for table in self.existing_relation:
            truncate_sql = f"DELETE FROM {table};"
            self.__execute(truncate_sql)
            try:
                drop_sql = f"DROP TABLE IF EXISTS {table};"
                self.__execute(drop_sql)
            except:
                print(f"Table {table} not exist. ")
        self.connection.commit()
    
    @__build_connection
    def execute(self, sql: str) -> List:
        return self.cursor.execute(sql)

    # @__build_connection
    def create_new_table(self) -> None:
        # Define the SQL command to create a new table with the desired schema
        table_schema = {
            "player": {
                "id": "VARCHAR",
                # "id": "VARCHAR PRIMARY KEY", # TODO: add primary key
            }, 

            "game": {
                "id": "VARCHAR",
                # "id": "VARCHAR PRIMARY KEY", # TODO: add primary key
                "player": "VARCHAR",
                "network_code": "CHAR",
            },
            "round": {
                "id": "VARCHAR",
                # "id": "VARCHAR PRIMARY KEY", # TODO: add primary key
                "game": "VARCHAR", 
                "tool_id": "CHAR",
                "round_number": "INT",
                "chosen_node": "CHAR",
                "payoff": "FLOAT",
            }
        }

        for table, schema in table_schema.items():
            _str_schema = ', '.join([f"{attr} {type}" for attr, type in schema.items()])
            create_table_sql = f'''
                CREATE TABLE IF NOT EXISTS {table} ({_str_schema});
            '''
            self.__execute(create_table_sql)

    @__build_connection
    def select(self, attribute: List[str]=["*"], relation: str="", condition: str="") -> List:
        assert relation in self.existing_relation.keys(), AssertionError("Relation not exist. ")

        query = f"SELECT {','.join(attribute)} FROM {relation} "
        if condition:
            query += f"WHERE {condition}"

        columns = [c[1] for c in self.__execute(f'PRAGMA table_info({relation})')] # fetch column names
        values = self.__execute(query).fetchall()
        return [
            {
                col: val for col, val in zip(columns, value)
            } for value in values
        ]

    @__build_connection
    def insert(self, mapping: Dict, relation: str) -> None:
        if relation not in self.existing_relation.keys():
            self.create_new_table()
        # assert relation in self.existing_relation.keys(), AssertionError("Relation not exist. ")
        columns = ", ".join(mapping.keys())
        values = ", ".join([f"\'{val}\'" for val in mapping.values()])
        query = f"INSERT INTO {relation} ({columns}) VALUES ({values})"
        try:
            self.__execute(query)
            self.connection.commit()
            print(f"Insertion success. ")
            print(f"Query: {query}\n")
        except:
            print(f"Insertion failed. ")
    
    @__build_connection
    def update(self, mapping: Dict, relation: str, pk: str) -> None:
        if relation not in self.existing_relation.keys():
            self.create_new_table()
        # assert relation in self.existing_relation.keys(), AssertionError("Relation not exist. ")
        content = ", ".join([f"{key} = '{val}'" for key, val in mapping.items()])
        query = f"UPDATE {relation} SET {content} WHERE id = '{pk}';"

        try:
            self.__execute(query)
            self.connection.commit()
        except:
            raise Exception("Update failed. ")
            



