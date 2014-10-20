import db_job_runner


import db_devices as model
import logging

import datetime
import uuid


class job_que_man(object):
    """The old Job Jueu code is getting confusing so this code is rewrite
    the job_que_should be simple abstraction to queing commands"""
    def __init__(self):
        self.log = logging.getLogger("uploaderFacade")
        self._job_runnerImp = None
        self._flags = None
        self.session = None
        self.job_class = None
        self.job_runner = db_job_runner.job_runner()
        self.job_runner.session = self.session
        
        
        
        
    def queue_length(self):
        output = 0
        return output
    

    def queue_dequeue(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        find_Update = session.query(model.UpdateInstance,model.UpdateType).\
                filter(model.UpdateInstance.expired == None).\
                filter(model.UpdateInstance.returncode == None).\
                filter(model.UpdateInstance.cmdln != None).\
                order_by(model.UpdateInstance.created)
        
        
        for item in find_Update:
            UpdateInstance = item[0]
            UpdateType = item[1]
            new_job_runner = db_job_runner.job_runner()
            new_job_runner.session = session
            new_job_runner.job_class = UpdateType.name
            new_job_runner.outputjson = UpdateInstance.outputjson
            new_job_runner.created = UpdateInstance.created
            new_job_runner.expires = UpdateInstance.expires
            new_job_runner.expired = UpdateInstance.expires
            
            new_job_runner.run(session = session)
            
            
            
            
            UpdateInstance.outputjson = new_job_runner.outputjson
            UpdateInstance.finished = datetime.datetime.now()
            UpdateInstance.returncode = new_job_runner.returncode
            #session.add(UpdateInstance)
            #session.commit()
        return None
    
    def jobtype_available(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("ddd")
            return
        outoup_set = set()
        job_types_query = session.query(model.UpdateType.name).all()
        output = []
        for item in job_types_query:
            output.append(item)
        return output
        
    def job_persist(self, *args, **kwargs):
        self.log.error("sssSSSSSSSssssssssssssssssSSSSSSSSSS")
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        job_type = kwargs.get('job_type', None)
        if job_type == None:
            self.log.error("kwargs 'job_type' missing")
            return False
        cmdln_template = kwargs.get('cmdln_template', None)
        if cmdln_template == None:
            self.log.error("kwargs 'cmdln_template' missing")
            return False
        cmdln_paramters = kwargs.get('cmdln_paramters', None)
        if cmdln_paramters == None:
            self.log.error("kwargs 'cmdln_paramters' missing")
            return False
        cmdln_paramters = kwargs.get('cmdln_paramters', None)
        if cmdln_paramters == None:
            self.log.error("kwargs 'cmdln_paramters' missing")
            return False
        name = kwargs.get('name', None)
        if name == None:
            self.log.warning("UpdateType_Add missing name")
            return
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.warning("unset self.session")
            return
        find_UpdateType = session.query(model.UpdateType).\
                filter(model.UpdateType.name == job_type)
        if find_UpdateType.count() == 0:
            newUpdateType = model.UpdateType()
            newUpdateType.name = job_type
            session.add(newUpdateType)
            session.commit()
            find_UpdateType = session.query(model.UpdateType).\
                filter(model.UpdateType.name == job_type)
        
        ret_job_type = find_UpdateType.one()
        
        find_Update = session.query(model.Update).\
                filter(model.Update.fk_type == ret_job_type.id).\
                filter(model.UpdateType.name == name).\
                filter(model.Update.cmdln_template == cmdln_template).\
                filter(model.Update.cmdln_paramters == cmdln_paramters)
                
        if find_Update.count() == 0:
            newUpdate = model.Update()
            newUpdate.fk_type = ret_job_type.id
            newUpdate.name = name
            newUpdate.cmdln_template = cmdln_template
            newUpdate.cmdln_paramters = cmdln_paramters
            
            session.add(newUpdate)
            session.commit()
            find_Update = session.query(model.Update).\
                filter(model.Update.fk_type == ret_job_type.id).\
                filter(model.UpdateType.name == name).\
                filter(model.Update.cmdln_template == cmdln_template).\
                filter(model.Update.cmdln_paramters == cmdln_paramters)
                
            
        if find_Update.count() != 1:
            self.log.error("Some thign bad happened")

        ret_job_details = find_Update.one()
        
        
        find_Update = session.query(model.UpdateInstance).\
                filter(model.UpdateInstance.fk_update == model.Update.id).\
                filter(model.Update.fk_type == ret_job_type.id).\
                filter(model.UpdateType.name == name).\
                filter(model.Update.cmdln_template == cmdln_template).\
                filter(model.Update.cmdln_paramters == cmdln_paramters)
                
        
        if find_Update.count() == 0:
            session.commit()
            print ret_job_details.id
            newUpdateInstance = model.UpdateInstance()
            print ret_job_details.id
            newUpdateInstance.fk_update == ret_job_details.id
            newUpdateInstance.name = name
            newUpdateInstance.created = datetime.datetime.now()
            newUpdateInstance.expires = datetime.datetime.now()
            newUpdateInstance.outputjson = None
            newUpdateInstance.returncode = None
            newUpdateInstance.fk_update = ret_job_details.id
            newUpdateInstance.uuid = str(uuid.uuid1())
            session.add(newUpdateInstance)
            session.commit()
def UpdateInstance_Run(self,session):
    find_existing = session.query(model.UpdateType,model.Update,model.UpdateInstance).\
        filter(model.UpdateInstance.expires < datetime.datetime.now()).\
        filter(model.Update.fk_type == model.UpdateType.id).\
        filter(model.UpdateInstance.fk_update == model.UpdateType.id)
    return find_existing
