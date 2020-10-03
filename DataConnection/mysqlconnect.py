import re
from sqlalchemy import Column, ForeignKey, orm, types
from sqlservice import declarative_base, event
from sqlservice import SQLClient
import sqlalchemy.dialects.mysql.pymysql

Model = declarative_base()


class User(Model):
    __tablename__ = 'user'

    id = Column(types.Integer(), primary_key=True)
    name = Column(types.String(100))
    email = Column(types.String(100))
    phone = Column(types.String(10))

    roles = orm.relation('UserRole')

    @event.on_set('phone', retval=True)
    def on_set_phone(self, value, oldvalue, initator):
        # Strip non-numeric characters from phone number.
        return re.sub('[^0-9]', '', value)


class UserRole(Model):
    __tablename__ = 'user_role'

    id = Column(types.Integer(), primary_key=True)
    user_id = Column(types.Integer(), ForeignKey('user.id'), nullable=False)
    role = Column(types.String(25), nullable=False)


config = {
    'SQL_DATABASE_URI': 'mysql+pymysql://root:monkeyxx@localhost:3306/stockData',
    'SQL_ISOLATION_LEVEL': 'SERIALIZABLE',
    'SQL_ECHO': True,
    'SQL_ECHO_POOL': False,
    'SQL_CONVERT_UNICODE': True,
    'SQL_POOL_SIZE': 5,
    'SQL_POOL_TIMEOUT': 30,
    'SQL_POOL_RECYCLE': 3600,
    'SQL_MAX_OVERFLOW': 10,
    'SQL_AUTOCOMMIT': False,
    'SQL_AUTOFLUSH': True,
    'SQL_EXPIRE_ON_COMMIT': True
}

db = SQLClient(config, model_class=Model)

db.create_all()

data = {'name': 'Jenny', 'email': 'jenny@example.com', 'phone': '555-867-5309'}
user = db.User.save(data)

assert user.to_dict() == {'id': 1,
                          'name': 'Jenny',
                          'email': 'jenny@example.com',
                          'phone': '5558675309'}

assert user is db.User.get(data.id)
assert user is db.User.find_one(id=user.id)
assert user is db.User.find(User.id == user.id)[0]

assert dict(user) == user.to_dict()

user.phone = '222-867-5309'
db.User.save(user)

assert user is db.User({'id': 1,
                        'name': 'Jenny',
                        'email': 'jenny@example.com',
                        'phone': '5558675309'})

db.User.destroy(user)
# OR db.User.destroy([user])
# OR db.User.destroy(user.id)
# OR db.User.destroy([user.id])
# OR db.User.destroy(dict(user))
# OR db.User.destroy([dict(user)])