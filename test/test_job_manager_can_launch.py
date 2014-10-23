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


import pmpmanager.db_devices as model
import pmpmanager.initialise_db as devices
import pmpmanager.job_exec as job_exec
import pmpmanager.job_manage as job_manage


import logging
import uuid

import tempfile



from sqlalchemy.orm import aliased


def debugger(session,uuid_execution):
    log = logging.getLogger("debugger")
    query_job_def = session.query(model.job_def).\
                filter(model.job_execution.uuid_job_execution == uuid_execution).\
                filter(model.job_def.id == model.job_execution.fk_update)
    
    
    log.debug("ssssssssssssssS")
    for item in query_job_def:
        log.error(item)


class Test_job_manager_can_launch(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("TestJobManager")
        
        f = tempfile.NamedTemporaryFile(delete=False)
        databaseConnectionString = "sqlite:///%s" % (f.name)
        
        
        self.engine = create_engine(databaseConnectionString, echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
    
    def test_CanLaunch(self):
        session = self.SessionFactory()
        new = job_manage.job_manage()
        new.session = session
        new.create_job_class(name = "lsblk_query")
        new_uuid1 = str(uuid.uuid1())
        new_uuid2 = str(uuid.uuid1())
        new_uuid3 = str(uuid.uuid1())
        debugger(session,new_uuid1)
        new.create_job_def(
                uuid=new_uuid1,
                job_class = "lsblk_query",
                cmdln_template = "ls",
                reocuring = 1,
            )
        
        job_detail = new.get_job_def(uuid = new_uuid1)
        job_detail.save()
        queue_count_before = job_detail.queue_count(session= session)
        self.assertTrue(queue_count_before == 0)
        job_state = job_detail.enqueue(
                session= session,
                uuid_task=new_uuid2,
                uuid_job=new_uuid3,
                cmdln_template="cmdln_template 1",
                reocuring=1,
                job_class="lsblk_query",
                cmdln_paramters="",
                uuid_job_def=new_uuid3,
                
            )
        query_job_namespace = session.query(model.job_execution).all()
        for i in query_job_namespace:
            self.log.error("query_job_namespace=%s" % (item))
        queue_count_after = job_detail.queue_count(session= session)
        self.log.error("%s!=%s" % (queue_count_before,queue_count_after))
        
        self.log.error("job_state=%s" % (job_state))
        query_job_def = session.query(model.job_execution).all()
        for item in query_job_def:
            self.log.error("ssssssssfffssssssS=%s" % (item))
        


if __name__ == "__main__":
    logging.basicConfig()
    LoggingLevel = logging.WARNING
    logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    nose.runmodule()
