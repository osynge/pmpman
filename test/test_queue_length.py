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



from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os.path
import os


import json


import pmpmanager.job_exec as job_exec
import pmpmanager.job_manage as job_manage


import logging
import uuid

import tempfile
import pmpmanager.db_job_queue as db_job_queue
from sqlalchemy.orm import aliased
import pmpmanager.initialise_db as devices
from uuid import uuid4 as uuidgen

class Test_job_manager_can_launch(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("TestJobManager")

        f = tempfile.NamedTemporaryFile(delete=False)
        databaseConnectionString = "sqlite:///%s" % (f.name)


        self.engine = create_engine(databaseConnectionString, echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        devices.initial_data_add_enumerated(self.SessionFactory())
        session = self.SessionFactory()
        jobmanager = job_manage.job_manage()
        jobmanager.session = session
        jobmanager.create_job_class(name = "lsblk_query")
        jobmanager.create_job_class(name = "lsblk_read")
        self.jobmanager_uuid1 = str(uuidgen())
        self.jobmanager_uuid2 = str(uuidgen())
        self.jobmanager_uuid3 = str(uuidgen())

        rc1 = jobmanager.create_job_def(
                uuid=self.jobmanager_uuid1,
                job_class = "lsblk_read",
                cmdln_template = "ls",
                reocuring = 1,
            )
        rc2 = jobmanager.create_job_def(
                uuid=self.jobmanager_uuid2,
                job_class = "lsblk_query",
                cmdln_template = "ls",
                reocuring = 1,
            )
        job_details1 = jobmanager.get_job_def(
            uuid = self.jobmanager_uuid1,
            session =session,
            )

        job_details2 = jobmanager.get_job_def(
            uuid = self.jobmanager_uuid1,
            session =session,
            )

        job_details1.save()
        job_details2.save()

    def test_setup_ok(self):
        session = self.SessionFactory()
        instance_query = session.query(model.job_def)
        self.assertTrue(1 < instance_query.count())


    def test_winglele(self):
        session = self.SessionFactory()
        instance_query = session.query(model.job_def)
        self.assertTrue(0 < instance_query.count())
        instance_query = session.query(model.job_execution)
        self.assertTrue(0 == instance_query.count())

        for item in instance_query:
            self.log.warning("item=%s" % (item.uuid_job_def))
            item.uuid_job_def ==  self.jobmanager_uuid1
            self.log.error(item.uuid_job_def)
            self.log.error(self.jobmanager_uuid1)


    def test_CanLaunch(self):
        session = self.SessionFactory()
        QM = db_job_queue.job_que_man()
        QM.session = session
        quelength = QM.queue_length(session = session)
        while quelength > 0:
            self.log.debug("cb_pmpman_block_scan:finished=%s" % (quelength))
            output = QM.queue_dequeue(session = session)
            quelength = quelength = QM.queue_length(session = session)
            time.sleep(10)


if __name__ == "__main__":
    logging.basicConfig()
    LoggingLevel = logging.WARNING
    logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    nose.runmodule()
