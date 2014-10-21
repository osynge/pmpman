import uuid
import sys
if sys.version_info < (2, 4):
    print "Your python interpreter is too old. Please consider upgrading."
    sys.exit(1)

if sys.version_info < (2, 5):
    import site
    import os.path
    from distutils.sysconfig import get_python_lib
    found = False
    module_dir = get_python_lib()
    for name in os.listdir(module_dir):
        lowername = name.lower()
        if lowername[0:10] == 'sqlalchemy' and 'egg' in lowername:
            sqlalchemy_dir = os.path.join(module_dir, name)
            if os.path.isdir(sqlalchemy_dir):
                site.addsitedir(sqlalchemy_dir)
                found = True
                break
    if not found:
        print "Could not find SQLAlchemy installed."
        sys.exit(1)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging

import db_devices as model
import datetime

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime
import lsblk
import json
import db_job_queue


def initial_data_add_job_state(session,name):
    state_new = model.job_state()
    state_new.name = name
    session.add(state_new)
    session.commit()

def initial_data_add_job_namespace(session,name):
    state_new = model.job_namespace()
    state_new.name = name
    session.add(state_new)
    session.commit()


def initial_data_add(session):
    for state in [
                    "create",
                    "pending"
                    "garbidge",
                    "executing",
                    "finished",
                ]:
        initial_data_add_job_state(session,state)
    for job_namespace in [
                    "no_ops",
                    "lsblk_query",
                    "lsblk_read"
                    "udev_query",
                    "udev_read",
                ]:
        initial_data_add_job_namespace(session,job_namespace)
    session.commit()
    import db_job_runner

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
    
    job_runner_lsblk.load(session = session)
    job_runner_lsblk_read.load(session = session)
    job_runner_udev_query.load(session = session)
    job_runner_lsblk.load(session = session)
    
    session.commit()
    
    job_runner_lsblk_read.subscribe_add(job_runner_lsblk.uuid_def)
    job_runner_lsblk_read.save(session = session)
    job_runner_udev_query.subscribe_add(job_runner_lsblk_read.uuid_def)
    job_runner_udev_query.save(session = session)
    job_runner_udev_read.subscribe_add(job_runner_udev_query.uuid_def)
    job_runner_udev_read.save(session = session)
    
    session.commit()
    
    job_runner_lsblk.enqueue(session = session)
    

class database_model:
    def __init__(self,databaseConnectionString):
        self.log = logging.getLogger("database_model")
        self.engine = create_engine(databaseConnectionString, echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        if self.CheckInittialisingNeeded():
            initial_data_add(self.SessionFactory())


        inital_quque = db_job_queue.job_que_man()
        inital_quque.session = self.SessionFactory()
        queue_length = inital_quque.queue_length()
        while queue_length > 0:
            inital_quque.queue_dequeue()
            queue_length = inital_quque.queue_length()

    def CheckInittialisingNeeded(self):
        session = self.SessionFactory()
        find_create_count = session.query(model.job_state).count()
        if find_create_count == 0:
            return True
        return False




    def Session(self):
        return self.SessionFactory()




    def job_namespace_Add(self, *args, **kwargs):
        name = kwargs.get('name', None)
        if name == None:
            self.log.warning("job_namespace_Add missing name")
            return
        session = kwargs.get('session', None)
        if session == None:
            session = self.SessionFactory()
        find_existing = session.query(model.job_namespace).\
                filter(model.job_namespace.name == name)
        if find_existing.count() >= 1:
            return
        newjob_namespace = model.job_namespace()
        newjob_namespace.name = name
        session.add(newjob_namespace)
        session.commit()

    def job_namespace_Run(self, *args, **kwargs):
        self.log.warning("job_namespace_Run")
        completed = False
        session = kwargs.get('session', None)
        if session == None:
            session = self.SessionFactory()

        find_existing = session.query(model.job_namespace).\
            filter(model.job_namespace.name == "lsblk")
        if find_existing.count() == 0:
            newjob_namespace = model.job_namespace()
            newjob_namespace.name = "lsblk"
            session.add(newjob_namespace)
            session.commit()
            find_existing = session.query(model.job_namespace).\
                filter(model.job_namespace.name == "lsblk")
        find_existing = session.query(model.job_namespace).\
            filter(model.job_namespace.name == "lsblk")
        if find_existing.count() == 0:
            self.log.warning("booo hooo")
            return
        updateType = find_existing.one()


        self.log.warning(updateType.name)

    def job_namespace_Clean(self, *args, **kwargs):
        name = kwargs.get('name', None)
        if name == None:
            self.log.warning("job_namespace_Clean missing name")
            return
        session = self.SessionFactory()
        find_existing_lsblk = session.query(model.job_namespace).\
                filter(model.job_namespace.name == "lsblk")
        if find_existing.count() == 0:
            self.log.warning("job_namespace_Clean missing name=lsblk")
            return
        newjob_namespace = model.job_namespace()
        newjob_namespace.name = name
        session.add(newjob_namespace)
        session.commit()

    def job_def_Add(self, *args, **kwargs):
        update_type = kwargs.get('update_type', None)
        if update_type == None:
            self.log.warning("job_def_Add missing update_type")
            return
        cammand_line = kwargs.get('cammand_line', None)
        if cammand_line == None:
            self.log.warning("job_def_Add missing cammand_line")
            return
        name = kwargs.get('name', None)
        if name == None:
            self.log.warning("job_def_Add missing name")
            return
        session = self.SessionFactory()
        find_existing = session.query(model.job_execution).\
                filter(model.job_namespace.name == update_type)
        if find_existing.count == 0:
            newjob_namespace = model.job_namespace()
            newjob_namespace.name = name
            session.add(newjob_namespace)
            session.commit()
            session = self.SessionFactory()
            find_existing = session.query(model.job_namespace).\
                filter(model.job_namespace.name == name)
            self.log.warning( find_existing.one())

    def job_def_Run(self, *args, **kwargs):
        update_type = kwargs.get('update_type', None)
        if update_type == None:
            self.log.warning("job_def_Add missing update_type")
            return
        session = kwargs.get('session', None)
        if session == None:
            session = self.SessionFactory()

        find_existing = session.query(model.job_namespace).\
            filter(model.job_namespace.name == "lsblk")
        if find_existing.count() == 0:
            self.log.warning("job_def_Add missing update_type")
            return
        id_job_namespace = int(find_existing.one().id)
        find_existing = session.query(model.job_def).\
            filter(model.job_namespace.id == id_job_namespace)
        if find_existing.count() == 0:
            self.log.info("no update found")
            newjob_def = model.job_def()
            newjob_def.created = datetime.datetime.now()
            newjob_def.expires = datetime.datetime.now()
            newjob_def.outputjson = None
            newjob_def.returncode = None
            newjob_def.fk_update = id_job_namespace
            session.add(newjob_def)
            session.commit()
        find_existing = session.query(model.job_def).\
            filter(model.job_namespace.id == id_job_namespace)

        id_job_def =None
        for item in find_existing:
            id_job_def = item.id


        find_existing = session.query(model.job_execution).\
            filter(model.job_def.id == id_job_def).\
            filter(model.job_execution.fk_update == model.job_def.id)
        if find_existing.count() == 0:
            self.log.warning("")
            find_update = session.query(model.job_def).\
                filter(model.job_namespace.name == "lsblk").\
                filter(model.job_def.fk_type == model.job_namespace.id)
            if find_update.count() == 0:
                pass
            newjob_def = model.job_execution()
            newjob_def.created = datetime.datetime.now()
            newjob_def.expires = datetime.datetime.now()
            newjob_def.outputjson = None
            newjob_def.returncode = None
            newjob_def.fk_update = id_job_namespace
            newjob_def.uuid = str(uuid.uuid1())
            newjob_def.triggers = '[]'
            session.add(newjob_def)
            session.commit()
            find_existing = session.query(model.job_namespace).\
                filter(model.job_namespace.name == "lsblk")
        find_existing = session.query(model.job_namespace).\
            filter(model.job_namespace.name == "lsblk")
        if find_existing.count() == 0:
            self.log.warning("booo hooo")
            return
        updateType = find_existing.one()



    def job_execution_Run_old(self, *args, **kwargs):
        self.log.debug('job_execution_Run')
        session = kwargs.get('session', None)
        if session == None:
            session = self.SessionFactory()
        find_existing = session.query(model.job_namespace,model.job_def,model.job_execution).\
            filter(model.job_execution.expires < datetime.datetime.now()).\
            filter(model.job_def.fk_type == model.job_namespace.id).\
            filter(model.job_execution.fk_update == model.job_namespace.id)
        if find_existing.count == 0:
            self.log.error("debug.job_execution_Run 0")
        for item in find_existing:
            item_type = item[0]
            update_instance = item[1]
            update_update = item[2]
            self.log.warning("item_type.name.=%s"  % (item_type.name))
            if item_type.name == "lsblk":
                output = lsblk.updatdatabase(session=session)
                #self.log.warning("newImage.devName=%s"  % (output))
                item_type.outputjson = output

                session.add(item_type)
                session.commit()
                self.job_def_Add(update_type="lsblkrc",)
            if item_type.name == "":
                pass
        session.commit()

    def job_execution_Run(self, *args, **kwargs):
        pass

