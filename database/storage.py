import sys
from dataclasses import dataclass
from datetime import date, datetime, time
from operator import itemgetter

allowed_dtypes = (str, int, float, date, datetime, time)

@dataclass
class TableColumn:
    name: str
    dtype: type
    unique: bool = False
    pkey: bool = False
    fkey: bool = False
    auto_incr: bool = False

    def __post_init__(self):
        if self.pkey: assert unique
        if self.auto_incr: assert dtype is int
        assert self.dtype in allowed_dtypes

        assert all(isinstance(self.__getattribute__(attr), dtype) for attr, dtype in self.__annotations__.items())


class Table:
    def __init__(self, name, *columns: tuple[TableColumn]):
        self.name = name
        self.columns = columns
        self.icolumns = {col.name: i for i, col in enumerate(columns)}
        self.unique_cols = tuple(col for col in columns if col.unique)
        self.data = []
    
    def insert(self, col_names, values):
        # assert valid column names
        assert all(col_name in [c.name for c in self.columns] for col_name in col_names)

        # assert unique
        # assert not any(any(tup[i] == row[i] for i in self.icolumns.values()) for row in self.data)
        
        # assert types
        assert all(isinstance(values[i], self.columns) for i, col in enumerate(self.columns))
        
        self.data.append(tup)


class DB:    
    @staticmethod
    def add_table(table):
        DB.__setattr__(table.name, table)


employees = Table(
    "Employee",
    TableColumn("id", int, True),
    TableColumn("name", str, False),
    TableColumn("salary", float, False)
)

employees.insert(("id", "name", "salary"), (1, "jonatan", 240.0))
employees.insert(("id", "name", "salary"), (2, "mia", 239.0))
