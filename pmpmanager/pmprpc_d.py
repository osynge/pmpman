import zerorpc

import initialise_db as  devices




from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import mapper

from sqlalchemy import ForeignKey

from sqlalchemy.orm import backref
try:
    from sqlalchemy.orm import relationship
except:
    from sqlalchemy.orm import relation as relationship

import uuid

from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os.path
import os

import tempfile
import initialise_db
import db_devices as model

def frog():
    pass
    


class fool(object):
    def count(self,number):
        return number


class HelloRPC(object):
    def __init__(self,db):
        self.db = db
    def hello(self, name):
        session = self.db.SessionFactory()
        query_subscribers = session.query(model.job_state).count()
        return "Hello, %s" % query_subscribers
    def dink(self,clientId):
        session = self.db.SessionFactory()
        query_subscribers = session.query(model.job_state).count()
        return "Hello, %s" % query_subscribers
        return 1
        
    def register_client(self,
        clientID,
        ):
        
        session = self.db.SessionFactory()
        query_client = session.query(model.client).\
                filter(clientID == model.client.uuid)
        if query_client.count() == 0:
            newclient = model.client()
            uuid_str = str(uuid.uuid1())
            newclient.uuid = uuid_str
            session.add(newclient)
            session.commit()
            return uuid_str
        for client in query_client:
            return client.uuid
    
            
            
    def registerd(self):
        session = self.db.SessionFactory()
        query_subscribers = session.query(model.client).count()
        
        uuid
        
        return "Hello, %s" % query_subscribers
        
databaseConnectionString = None



class dbconnection(object):
    def dbconnectionstring_set_random(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        self.databaseConnectionString = "sqlite:///%s" % (f.name)
        
    def setup(self):
        self.engine = create_engine(self.databaseConnectionString, echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        initialise_db.initial_data_add_enumerated(self.SessionFactory())
    
    
db = dbconnection()
db.dbconnectionstring_set_random()
db.setup()

s = zerorpc.Server(HelloRPC(db))
s.bind("tcp://0.0.0.0:4242")
s.run()


