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
import pmpmanager.initialise_db as  devices
import pmpmanager.job_exec as job_exec
import pmpmanager.job_manage as job_manage


import logging
import uuid

import tempfile



from sqlalchemy.orm import aliased


class TestJobRunnerFacard(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("TestJobManager")
        
        f = tempfile.NamedTemporaryFile(delete=False)
        databaseConnectionString = "sqlite:///%s" % (f.name)
        
        
        self.engine = create_engine(databaseConnectionString, echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        devices.initial_data_add_enumerated(self.SessionFactory())
     
    def test_zzzz(self):
        session = self.SessionFactory()
        new = job_manage.job_manage()
        new.session = session
        self.log.error(new.list_job_class())
        self.log.error(new.list_job_def())
    
    def test_exec(self):
        session = self.SessionFactory()
        new = job_manage.job_manage()
        new.session = session
        new.create_job_class(name = "lsblk_query")
        new_uuid = str(uuid.uuid1())
        new.create_job_def(
                uuid=new_uuid,
                job_class = "lsblk_query",
                cmdln_template = "ls",
                reocuring = 1,
            )
        
        jobtmplate = new.get_job_def(uuid=new_uuid)
        self.assertTrue(jobtmplate != None)
        jobtmplate.run()
        self.log.error(jobtmplate.subscribe_list)
        

        
    
    

    def test_showjobs(self):
        session = self.SessionFactory()
        new = job_manage.job_manage()
        new.session = session
        job_list = new.list_job_def()
        for item in job_list:
            #self.log.debug("jobid=%s" % (item))
            job_details = new.show_job_def(uuid = item)
            #self.log.error("job_details=%s" % (job_details))
    
            
    def test_create_job_def(self):
        session = self.SessionFactory()
        new = job_manage.job_manage()
        
        
        
        
        new.session = session
        new.create_job_class(name = "lsblk_query")
        new_uuid = str(uuid.uuid1())
        before = len(new.list_job_def())
        new.create_job_def(
                uuid=new_uuid,
                job_class = "lsblk_query",
                cmdln_template = "ls",
                reocuring = 1,
            )
        after = len(new.list_job_def())
        self.assertTrue(after-before == 1)



    
        

    def test_job_def_save_retrive_subscribe_list(self):
        session = self.SessionFactory()
        new = job_manage.job_manage()
        new.session = session
        new.create_job_class(name = "lsblk_query")
        new_uuid1 = str(uuid.uuid1())
        new_uuid2 = str(uuid.uuid1())
        
        new.create_job_def(
                uuid=new_uuid1,
                job_class = "lsblk_query",
                cmdln_template = "ls",
                reocuring = 1,
            )
        new.create_job_def(
                uuid=new_uuid2,
                job_class = "lsblk_query",
                cmdln_template = "ls",
                reocuring = 1,
            )
        job_details1 = new.get_job_def(uuid = new_uuid1)
        job_details2 = new.get_job_def(uuid = new_uuid2)
        self.assertTrue(len(job_details1.publish_list) == 0)
        self.assertTrue(len(job_details2.publish_list) == 0)
        job_details1.publish_list = set([new_uuid2])
        job_details1.subscribe_list = set([new_uuid2])
        
        self.assertTrue(len(job_details1.subscribe_list) == 1)
        job_details1.save()
        self.assertTrue(len(job_details1.subscribe_list) == 1)
        job_details2.save()
        self.assertTrue(len(job_details1.subscribe_list) == 1)
        
        #source_job = aliased(model.job_def, name='source_job')
        #dest_job = aliased(model.job_def, name='dest_job')
        
        #query_subscribers = session.query(dest_job).\
        #        filter(source_job.uuid == new_uuid2).\
        #        filter(model.job_triggers.dest == dest_job.id).\
        #        filter(model.job_triggers.source == source_job.id)
        
        #self.log.warning("c1=%s" % (query_subscribers.count()))
        #for item in query_subscribers:
        #    self.log.warning("item=%s" % (item))
        
        
        #query_publishers = session.query(source_job).\
        #        filter(source_job.uuid == new_uuid2).\
        #        filter(model.job_triggers.dest == dest_job.id).\
        #        filter(model.job_triggers.source == source_job.id)

        #self.log.warning("c2=%s" % (query_publishers.count()))
        #for item in query_publishers:
        #    self.log.warning("item=%s" % (item))
        
        
        job_details1.load()
        self.assertTrue(len(job_details1.subscribe_list) == 1)
        job_details2.load()
        self.assertTrue(len(job_details1.subscribe_list) == 1)
        self.assertTrue(len(job_details1.publish_list) == 1)
        self.assertTrue(len(job_details2.subscribe_list) == 1)
        self.assertTrue(len(job_details2.publish_list) == 1)
        



if __name__ == "__main__":
    logging.basicConfig()
    LoggingLevel = logging.WARNING
    logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    nose.runmodule()
