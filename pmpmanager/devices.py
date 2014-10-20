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



class database_model:
    def __init__(self,databaseConnectionString):
        self.log = logging.getLogger("database_model")
        self.engine = create_engine(databaseConnectionString, echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
    
    
    def Session(self):
        return self.SessionFactory()
    
        


    def UpdateType_Add(self, *args, **kwargs):
        name = kwargs.get('name', None)
        if name == None:
            self.log.warning("UpdateType_Add missing name")
            return
        session = kwargs.get('session', None)
        if session == None:
            session = self.SessionFactory()
        find_existing = session.query(model.UpdateType).\
                filter(model.UpdateType.name == name)
        if find_existing.count() >= 1:
            return
        newUpdateType = model.UpdateType()
        newUpdateType.name = name
        session.add(newUpdateType)
        session.commit()
        
    def UpdateType_Run(self, *args, **kwargs):
        self.log.warning("UpdateType_Run")
        completed = False
        session = kwargs.get('session', None)
        if session == None:
            session = self.SessionFactory()
        
        find_existing = session.query(model.UpdateType).\
            filter(model.UpdateType.name == "lsblk")
        if find_existing.count() == 0:
            newUpdateType = model.UpdateType()
            newUpdateType.name = "lsblk"
            session.add(newUpdateType)
            session.commit()
            find_existing = session.query(model.UpdateType).\
                filter(model.UpdateType.name == "lsblk")
        find_existing = session.query(model.UpdateType).\
            filter(model.UpdateType.name == "lsblk")
        if find_existing.count() == 0:
            self.log.warning("booo hooo")
            return
        updateType = find_existing.one()
        
        
        self.log.warning(updateType.name)
        
    def UpdateType_Clean(self, *args, **kwargs):
        name = kwargs.get('name', None)
        if name == None:
            self.log.warning("UpdateType_Clean missing name")
            return
        session = self.SessionFactory()
        find_existing_lsblk = session.query(model.UpdateType).\
                filter(model.UpdateType.name == "lsblk")
        if find_existing.count() == 0:
            self.log.warning("UpdateType_Clean missing name=lsblk")
            return
        newUpdateType = model.UpdateType()
        newUpdateType.name = name
        session.add(newUpdateType)
        session.commit()

    def Update_Add(self, *args, **kwargs):
        update_type = kwargs.get('update_type', None)
        if update_type == None:
            self.log.warning("Update_Add missing update_type")
            return
        cammand_line = kwargs.get('cammand_line', None)
        if cammand_line == None:
            self.log.warning("Update_Add missing cammand_line")
            return
        name = kwargs.get('name', None)
        if name == None:
            self.log.warning("Update_Add missing name")
            return
        session = self.SessionFactory()
        find_existing = session.query(model.job_execution).\
                filter(model.UpdateType.name == update_type)
        if find_existing.count == 0:
            newUpdateType = model.UpdateType()
            newUpdateType.name = name
            session.add(newUpdateType)
            session.commit()
            session = self.SessionFactory()
            find_existing = session.query(model.UpdateType).\
                filter(model.UpdateType.name == name)
            self.log.warning( find_existing.one())

    def Update_Run(self, *args, **kwargs):
        update_type = kwargs.get('update_type', None)
        if update_type == None:
            self.log.warning("Update_Add missing update_type")
            return
        session = kwargs.get('session', None)
        if session == None:
            session = self.SessionFactory()
        
        find_existing = session.query(model.UpdateType).\
            filter(model.UpdateType.name == "lsblk")
        if find_existing.count() == 0:
            self.log.warning("Update_Add missing update_type")
            return
        id_UpdateType = int(find_existing.one().id)
        find_existing = session.query(model.Update).\
            filter(model.UpdateType.id == id_UpdateType)
        if find_existing.count() == 0:
            self.log.info("no update found")
            newUpdate = model.Update()
            newUpdate.created = datetime.datetime.now()
            newUpdate.expires = datetime.datetime.now()
            newUpdate.outputjson = None
            newUpdate.returncode = None
            newUpdate.fk_update = id_UpdateType
            session.add(newUpdate)
            session.commit()
        find_existing = session.query(model.Update).\
            filter(model.UpdateType.id == id_UpdateType)
        
        id_Update =None
        for item in find_existing:
            id_Update = item.id
        
        
        find_existing = session.query(model.job_execution).\
            filter(model.Update.id == id_Update).\
            filter(model.job_execution.fk_update == model.Update.id)
        if find_existing.count() == 0:
            self.log.warning("")
            find_update = session.query(model.Update).\
                filter(model.UpdateType.name == "lsblk").\
                filter(model.Update.fk_type == model.UpdateType.id)
            if find_update.count() == 0:
                pass
            newUpdate = model.job_execution()
            newUpdate.created = datetime.datetime.now()
            newUpdate.expires = datetime.datetime.now()
            newUpdate.outputjson = None
            newUpdate.returncode = None
            newUpdate.fk_update = id_UpdateType
            newUpdate.uuid = str(uuid.uuid1())
            newUpdate.triggers = '[]'
            session.add(newUpdate)
            session.commit()
            find_existing = session.query(model.UpdateType).\
                filter(model.UpdateType.name == "lsblk")
        find_existing = session.query(model.UpdateType).\
            filter(model.UpdateType.name == "lsblk")
        if find_existing.count() == 0:
            self.log.warning("booo hooo")
            return
        updateType = find_existing.one()
        

        
    def job_execution_Run_old(self, *args, **kwargs):
        self.log.debug('job_execution_Run')
        session = kwargs.get('session', None)
        if session == None:
            session = self.SessionFactory()
        find_existing = session.query(model.UpdateType,model.Update,model.job_execution).\
            filter(model.job_execution.expires < datetime.datetime.now()).\
            filter(model.Update.fk_type == model.UpdateType.id).\
            filter(model.job_execution.fk_update == model.UpdateType.id)
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
                self.Update_Add(update_type="lsblkrc",)
            if item_type.name == "":
                pass
        session.commit()
        
    def job_execution_Run(self, *args, **kwargs):
        pass
        
