from os import environ
from sqlalchemy import create_engine


class DBConnect:
    db_uri = 'mysql+pymysql://root:monkeyxx@localhost:3306/stockData'
    engine = create_engine(db_uri, echo=True)
    table = 'stockData'
