from pmpmanager.db_job_runner import job_runner, InputError

import unittest



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
import logging

class TestJobRunnerFacard(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("TestJobRunnerFacard")
        databaseConnectionString = 'sqlite:///pmpman_test.db'
        self.engine = create_engine(databaseConnectionString, echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        
        
    def test_session_set(self):
        session = self.SessionFactory()
        new = job_runner()
        new.session = session
        self.assertTrue(new.session == session)


    def test_job_class_set_no_session(self):

        new = job_runner()
        raised_exception = 0
        try:
            new.job_class = "dd"
        except InputError:
            raised_exception += 1
        self.assertTrue(raised_exception == 1)
        
        
    def test_job_class_set(self):
        new = job_runner()
        new.job_class = "no_ops"
        new.job_class = "lsblk_query"
        new.job_class = "lsblk_read"
        
        for allowed_class in [ "no_ops","kname_new", "udev_query" , "lsblk_query" , "lsblk" , "udev_read" ,"lsblk_read" ]:
            self.log.debug(allowed_class)
            new.job_class = allowed_class
            self.log.debug(new.job_class)
