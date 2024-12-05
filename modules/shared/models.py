from sqlalchemy import create_engine, String, Column, Integer, Text, Boolean, ForeignKey, TIMESTAMP, DECIMAL, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

Base = declarative_base()
session = sessionmaker()
engine = create_engine('postgresql://postgres:password@localhost/dinner_db')
# engine = create_engine('postgresql://dinner_db_user:yjE5j4sSC1HAZIdwSvXIDFBjGy5ogFUV@dpg-css1vuhu0jms73e4tnl0-a.oregon-postgres.render.com/dinner_db')
session = session(bind = engine)

def generate_uuid():
    return str(uuid.uuid4())
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_church = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False) 
    is_bouncer = Column(Boolean, default=False)
    created_on = Column(TIMESTAMP, default=datetime.now)

    guess = relationship('Guest', back_populates='user')

    def __repr__(self):
        return f"<User({self.id}, {self.email}, {self.is_active})>"

class Guest(Base):
    __tablename__ = 'guests'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    church = Column(Integer, ForeignKey('users.id'))
    attendance_status = Column(Integer, ForeignKey('statuses.id'))
    table = Column(Integer, ForeignKey('table_types.id'))

    user = relationship('User', back_populates='guess')
    status = relationship('Status', back_populates='guess')
    table_type = relationship('TableType', back_populates='guess')

    def __repr__(self):
        return f"<Guest({self.id}, {self.full_name}, {self.email}, {self.phone_number}, {self.church}, {self.attendance_status}, {self.table})>"


class TableType(Base):
    __tablename__ = 'table_types'
    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)

    guess = relationship('Guest', back_populates='table_type')

    def __repr__(self):
        return f"<TableType({self.id}, {self.type})>"



class Status(Base):
    __tablename__ ='statuses'
    id = Column(Integer, primary_key=True)
    status = Column(String(255), nullable=False)

    guess = relationship('Guest', back_populates='status')

    def __repr__(self):
        return f"<Status({self.id}, {self.status})>"

# Create tables
Base.metadata.create_all(engine)