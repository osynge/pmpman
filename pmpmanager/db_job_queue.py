import db_job_runner


import db_devices as model
import logging

import datetime
import uuid
import json
import string

class job_que_man(object):
    """The old Job Jueu code is getting confusing so this code is rewrite
    the job_que_should be simple abstraction to queing commands"""
    def __init__(self):
        self.log = logging.getLogger("job_que_man")
        self._job_runnerImp = None
        self._flags = None
        self.session = None
        self.job_class = None
        self.job_runner = db_job_runner.job_runner()
        self.job_runner.session = self.session
        
        
        
        
    def queue_length(self):
        output = 0
        return output
    
    
    def queue_read(self, *args, **kwargs):
        session = kwargs.get('queue_read', None)
        if session == None:
            session = self.session
        
        find_Update = session.query(model.UpdateInstance,model.Update,model.UpdateType).\
                filter(model.UpdateInstance.fk_update == model.Update.id).\
                filter(model.Update.fk_type == model.UpdateType.id).\
                order_by(model.UpdateInstance.created)
        self.log.debug('find_Update.count=%s' % find_Update.count())
        for item in find_Update:
            UpdateInstance = item[0]
            UpdateType = item[2]
            Update =  item[1]
            
            tridggeres = json.loads ( UpdateInstance.triggers)
            #self.log.error('tridggeres=%s' % tridggeres)
            params = json.loads ( UpdateInstance.trig_parameters)
            for trig in tridggeres:
                self.log.error('trig=%s' % trig)
                
                update_query = session.query(model.Update).\
                    filter(model.Update.fk_type == model.UpdateType.id).\
                    filter(model.UpdateType.name == trig)
                self.log.error('count=%s' % update_query.count())
                for target in update_query:
                    fk_update = target.id
                    self.log.error('target.id=%s' % target.id)
                    new_cmdln = string.Template(target.cmdln_template).substitute(para)
                    self.log.info('new_cmdln=%s' % new_cmdln)
                    self.log.info('para=%s' % para)
                    newUpdateInstance = model.UpdateInstance()
                    newUpdateInstance.fk_update = target.id
                    newUpdateInstance.name = ""
                    newUpdateInstance.created = datetime.datetime.now()
                    newUpdateInstance.expires = datetime.datetime.now()
                    newUpdateInstance.outputjson = None
                    newUpdateInstance.returncode = None
                    newUpdateInstance.uuid = str(uuid.uuid1())
                    newUpdateInstance.triggers = "[]"
                    newUpdateInstance.cmdln = new_cmdln
                    session.add(newUpdateInstance)
                    session.commit()

                
                
                
    def queue_dequeue(self, *args, **kwargs):
        self.log.debug('queue_dequeue')
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        find_Update = session.query(model.UpdateInstance,model.UpdateType).\
                filter(model.UpdateInstance.expired == None).\
                filter(model.UpdateInstance.returncode == None).\
                order_by(model.UpdateInstance.created)
        #self.log.error('queue_dequeue=%s' % find_Update.count())
        
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
            UpdateInstance.finshed = datetime.datetime.now()
            UpdateInstance.returncode = new_job_runner.returncode
            UpdateInstance.cmdln = new_job_runner.cmdln
            UpdateInstance.triggers = new_job_runner.triggers
            UpdateInstance.trig_parameters = new_job_runner.trig_parameters
            
            session.add(UpdateInstance)
            session.commit()
        
        
        self.queue_read(session = session)
            
        return None
        
        
        
    def initialise(self, *args, **kwargs) : 
        session = kwargs.get('initialise', None)
        if session == None:
            session = self.session
        new_job_runner = db_job_runner.job_runner()
        new_job_runner.session = session
        for i in new_job_runner.job_classes.keys():
            new_job_runner.job_class = i
            new_job_runner.save()
            
    def jobtype_available(self, *args, **kwargs):
        session = kwargs.get('jobtype_available', None)
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
        job_uuid = kwargs.get('uuid', None)
        if job_uuid  == None:
            self.log.debug("No UUID specified")
            job_uuid = str(uuid.uuid4())
       
        
        
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
            newUpdate.uuid = job_uuid
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
            newUpdateInstance = model.UpdateInstance()
            newUpdateInstance.fk_update == ret_job_details.id
            newUpdateInstance.name = name
            newUpdateInstance.created = datetime.datetime.now()
            newUpdateInstance.expires = datetime.datetime.now()
            newUpdateInstance.outputjson = None
            newUpdateInstance.returncode = None
            newUpdateInstance.fk_update = ret_job_details.id
            newUpdateInstance.uuid = str(uuid.uuid1())
            newUpdateInstance.triggers = "[]"
            session.add(newUpdateInstance)
            session.commit()
def UpdateInstance_Run(self,session):
    find_existing = session.query(model.UpdateType,model.Update,model.UpdateInstance).\
        filter(model.UpdateInstance.expires < datetime.datetime.now()).\
        filter(model.Update.fk_type == model.UpdateType.id).\
        filter(model.UpdateInstance.fk_update == model.UpdateType.id)
    return find_existing
