import sys, os


sys.path = [os.path.abspath(os.path.dirname(os.path.dirname(__file__)))] + sys.path


import unittest
import nose

import pmpmanager.job_exec  


import pmpmanager.initialise_db as devices

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

import pmpmanager.db_devices as model

import pmpmanager.initialise_db as devices



import pmpmanager.job_exec as job_exec


import json

lsblk_wantedFields = ["NAME","KNAME","MOUNTPOINT","PARTUUID","SERIAL","FSTYPE","RM","SIZE","FSTYPE","UUID","OWNER","GROUP","MODE","WWN","VENDOR","MAJ:MIN"]


from uuid import uuid4 as uuidgen
import logging
import tempfile

class TestJobExec(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("TestJobExec")
        f = tempfile.NamedTemporaryFile(delete=False)
        databaseConnectionString = "sqlite:///%s" % (f.name)
        self.engine = create_engine(databaseConnectionString, echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        session = self.SessionFactory()
        #Set up data base
        devices.test_CanLaunch(session)
        
        
    def test_session_set(self):
        session = self.SessionFactory()
        new = job_exec.job_exec(session = session)
        new.session = session
        
        new_uuid1 = str(uuidgen())
        new_uuid2 = str(uuidgen())
        new_uuid3 = str(uuidgen())
        new.job_class = "lsblk_query"
        self.assertTrue(new.job_class == "lsblk_query")
        new.save(
            session=session,
            uuid_tempate=new_uuid1,
            uuid_execution=new_uuid2,
            cmdln_template=new_uuid3,
            cmdln_paramters="",
            uuid_job_def="",
            )
        
    
    def test_exec(self):
        session = self.SessionFactory()
        new = job_exec.job_exec()
        new.session = session
        new.job_class = "lsblk_query"
        new.cmdln = "lsblk  --output %s  --pairs" % ( ",".join(lsblk_wantedFields) )
        new.run(session = session)
        fred = json.loads(new.outputjson)
        
        self.log.debug(fred)
        
    
    
    def test_save(self):
        session = self.SessionFactory()
        new = job_exec.job_exec()
        new.session = session
        new_uuid1 = str(uuidgen())
        new_uuid2 = str(uuidgen())
        new_uuid3 = str(uuidgen())
        new.job_class = "lsblk_query"
        new.cmdln = "lsblk  --output %s  --pairs" % ( ",".join(lsblk_wantedFields) )
        new.save(
            session=session,
            uuid_tempate=new_uuid1,
            uuid_execution=new_uuid2,
            cmdln_template=new_uuid3,
            cmdln_paramters="",
            uuid_job_def="",

            )
        #fred = json.loads(new.outputjson)
        #self.log.debug(fred) 
    def test_lsblk_read(self):
        
        session = self.SessionFactory()
        writer = job_exec.job_exec()
        writer.session = session
        new_uuid1 = str(uuidgen())
        new_uuid2 = str(uuidgen())
        new_uuid3 = str(uuidgen())
        writer.job_class = "lsblk_query"
        writer.cmdln = "lsblk  --output %s  --pairs" % ( ",".join(lsblk_wantedFields) )
        writer.save(
            session=session,
            uuid_tempate=new_uuid1,
            uuid_execution=new_uuid2,
            cmdln_template=new_uuid3,
            cmdln_paramters="",
            uuid_job_def="",
            )
        reader = job_exec.job_exec()
        reader.session = session
        reader.job_class = "lsblk_query"
        reader.cmdln = ""
        reader.save(
            session=session,
            uuid_tempate=new_uuid1,
            uuid_execution=new_uuid2,
            cmdln_template=new_uuid3,
            cmdln_paramters="",
            uuid_job_def="",
            )
        new = job_exec.job_exec()
        reader.session = session
        

if __name__ == "__main__":
    logging.basicConfig()
    LoggingLevel = logging.WARNING
    logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    nose.runmodule()

