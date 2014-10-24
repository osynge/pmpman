import sys, os


sys.path = [os.path.abspath(os.path.dirname(os.path.dirname(__file__)))] + sys.path


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

import string

from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os.path
import os


import json


import pmpmanager.db_devices as model
import pmpmanager.initialise_db as  initialise_db
import pmpmanager.job_exec as job_exec
import pmpmanager.job_manage as job_manage
import pmpmanager.job_threadpool as job_threadpool

import logging
import uuid

import tempfile


from uuid import uuid4 as uuidgen
from sqlalchemy.orm import aliased

def testcbDone():
    log = logging.getLogger("testcbDone")
    log.error("called")


lsblk_wantedFields = ["NAME","KNAME","MOUNTPOINT","PARTUUID","SERIAL","FSTYPE","RM","SIZE","FSTYPE","UUID","OWNER","GROUP","MODE","WWN","VENDOR","MAJ:MIN"]


class TestJobRunnerFacard(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("TestJobManager")

        f = tempfile.NamedTemporaryFile(delete=False)
        databaseConnectionString = "sqlite:///%s" % (f.name)


        self.engine = create_engine(databaseConnectionString, echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        initialise_db.initial_data_add_enumerated(self.SessionFactory())

    def test_threadpool(self):
        session = self.SessionFactory()
        new = job_manage.job_manage()
        new.session = session
        self.log.error(new.list_job_class())
        self.log.error(new.list_job_def())

        tp = job_threadpool.threadpool_jobs(2)
        import time
        tp.SendMessage(testcbDone,"msg")
        tp.SendMessage(testcbDone,"msg")
        tp.SendMessage(testcbDone,"msg")

        #job_json = ""
        #tp.EnqueJob(job_json)
        #log.error('self.tasks.qsize=%s' % (  tp.tasks.qsize()))
        tp.wait_completion()



    def test_threadpool_exec(self):

        writer = job_exec.job_exec()
        new_uuid1 = str(uuidgen())
        new_uuid2 = str(uuidgen())
        new_uuid3 = str(uuidgen())
        writer.job_class = "lsblk_query"
        writer.cmdln = "lsblk  --output %s  --pairs" % ( ",".join(lsblk_wantedFields) )
        writer.run(
            uuid_tempate=new_uuid1,
            uuid_execution=new_uuid2,
            cmdln_template=new_uuid3,
            cmdln_paramters="",
            uuid_job_def="",
            )




if __name__ == "__main__":
    logging.basicConfig()
    LoggingLevel = logging.WARNING
    logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    nose.runmodule()
