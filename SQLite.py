# https://docs.python.org/3/library/sqlite3.html
import sqlite3
from typing import List, Dict

class oTreeSQLite:
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None
        self.existing_relation = self.__fetch_existing_table()

    def __execute(self, sql: str) -> List:
        return self.cursor.execute(sql)
    
    def __build_connection(func):
        def wrapper(self, *args, **kwargs):
            self.connection = sqlite3.connect('db.sqlite3')
            self. cursor = self.connection.cursor()
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
    def execute(self, sql: str) -> List:
        return self.cursor.execute(sql)

    @__build_connection
    def select(self, attribute: List[str]=["*"], relation: str="", condition: str="") -> List:
        assert relation in self.existing_relation.keys(), AssertionError("Relation not exist. ")

        query = f"SELECT {','.join(attribute)} FROM {relation} "
        if condition:
            query += f"WHERE {condition}"

        columns = [c[1] for c in self.__execute('PRAGMA table_info(build_for_test_player)')] # fetch column names
        values = self.__execute(query).fetchall()
        return [
            {
                col: val for col, val in zip(columns, value)
            } for value in values
        ]

    @__build_connection
    def insert(self, mapping: Dict, relation: str) -> None:
        assert relation in self.existing_relation.keys(), AssertionError("Relation not exist. ")
        values = tuple(mapping.values())
        query = f"INSERT INTO {relation} VALUES {values}"
        # self.connection.close()
        self.__execute(query)
        self.connection.commit()