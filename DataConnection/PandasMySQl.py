from sqlalchemy.types import Integer, Text, String, DateTime, Float
from DataConnection.dbconnect import DBConnect
import pandas as pd


class DFDBObject:
    data = pd.DataFrame()
    engine = DBConnect.engine
    table = DBConnect.table

    def __init__(self, data):
        self.data = data


    def SendToDB(self):
        datatypes = self.GetDataTypes()

        self.data.to_sql(
            self.table,
            self.engine,
            if_exists='replace',
            index=False,
            chunksize=500,
            dtype=datatypes
        )

    def GetDataTypes(self):
        datatypes = {self.data.index.name: "int"}
        types = self.data.dtypes
        columns = self.data.columns

        for col, dtype in zip(columns, types):
            datatypes.update({col: str(dtype)})
        return datatypes
