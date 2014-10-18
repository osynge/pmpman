from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import mapper

from sqlalchemy import ForeignKey

from sqlalchemy.orm import backref
try:
    from sqlalchemy.orm import relationship
except:
    from sqlalchemy.orm import relation as relationship


from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

from sqlalchemy.schema import UniqueConstraint
##########################################
# makes key value tables to increase flexibility.

Base = declarative_base()


class USB_Bus_Hw(Base):
    __tablename__ = 'USB_Bus_Hw'
    id = Column(Integer, primary_key=True)
    idVendor = Column(String(100),nullable = False,unique=True)
    idProduct = Column(String(100),nullable = False,unique=True)
    
    def __init__(self,subject):
        self.idVendor = subject
    def __repr__(self):
        return "<USB_Bus_Hw('%s')>" % (self.subject)

def init(engine):
    Base.metadata.create_all(engine)
