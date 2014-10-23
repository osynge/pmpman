import sys, os
sys.path = [os.path.abspath(os.path.dirname(os.path.dirname(__file__)))] + sys.path
from pmpmanager.db_job_runner import job_runner, InputError
import unittest
import nose
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
import pmpmanager.db_job_runner  as db_job_runner

import tempfile
import logging


class TestJobRunnerFacard(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("TestJobRunnerFacard")
        
        f = tempfile.NamedTemporaryFile(delete=False)
        databaseConnectionString = "sqlite:///%s" % (f.name)
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


    def test_job_initalise(self):
        session = self.SessionFactory()
        for state in [
                        "create",
                        "pending"
                        "garbidge",
                        "executing",
                        "finished",
                    ]:
            devices.initial_data_add_job_state(session,state)
        for job_namespace in [
                        "no_ops",
                        "lsblk_query",
                        "lsblk_read"
                        "udev_query",
                        "udev_read",
                    ]:
            devices.initial_data_add_job_namespace(session,job_namespace)
        session.commit()

        job_runner_lsblk = db_job_runner.job_runner()
        job_runner_lsblk.job_class = "lsblk_query"
        job_runner_lsblk.uuid_def = "3b201cc5-897c-49c7-87e2-5eaddc31c0c3"
        job_runner_lsblk.name = "lsblk_query"
        job_runner_lsblk.save(session = session)



        job_runner_lsblk_read = db_job_runner.job_runner()
        job_runner_lsblk_read.job_class = "lsblk_read"
        job_runner_lsblk_read.uuid_def = "6d7141d5-e1ee-4ff6-a778-10803521c8a2"
        job_runner_lsblk_read.name = "lsblk_read"
        job_runner_lsblk_read.save(session = session)

        job_runner_udev_query = db_job_runner.job_runner()
        job_runner_udev_query.job_class = "udev_query"
        job_runner_udev_query.uuid_def = "c297b566-089d-4895-a8c2-a9cc37767174"
        job_runner_udev_query.name = "udev_query"
        job_runner_udev_query.save(session = session)

        job_runner_udev_read = db_job_runner.job_runner()
        job_runner_udev_read.job_class = "udev_read"
        job_runner_udev_read.uuid_def = "b9c94c0e-7dc8-4434-9355-e6cb4835fb63"
        job_runner_udev_read.name = "udev_read"
        job_runner_udev_read.save(session = session)

        session.commit()


        job_runner_lsblk_read.subscribe_add(job_runner_lsblk.uuid_def)
        job_runner_lsblk_read.save(session = session)
        job_runner_udev_query.subscribe_add(job_runner_lsblk_read.uuid_def)
        job_runner_udev_query.save(session = session)
        job_runner_udev_read.subscribe_add(job_runner_udev_query.uuid_def)
        job_runner_udev_read.save(session = session)

        session.commit()

        job_runner_lsblk.enqueue(session = session)


if __name__ == "__main__":
    logging.basicConfig()
    LoggingLevel = logging.WARNING
    logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    nose.runmodule()
