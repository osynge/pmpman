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
        
    def initialise(self, *args, **kwargs) : 
        
        session = kwargs.get('initialise', None)
        if session == None:
            session = self.session
        new_job_runner = db_job_runner.job_runner()
        new_job_runner.session = session
        for i in new_job_runner.job_classes.keys():
            new_job_runner.job_class = i
            new_job_runner.save()
                
        
        
    def queue_length(self):
        output = 0
        return output
        find_job_def = session.query(model.job_def).\
            filter(model.job_execution.fk_update == model.job_def.id)
    
    def queue_read(self, *args, **kwargs):
        session = kwargs.get('queue_read', None)
        if session == None:
            session = self.session
        
        find_job_def = session.query(model.job_execution,model.job_def,model.job_namespace).\
                filter(model.job_execution.fk_update == model.job_def.id).\
                filter(model.job_def.fk_type == model.job_namespace.id).\
                order_by(model.job_execution.created)
        self.log.debug('find_job_def.count=%s' % find_job_def.count())
        for item in find_job_def:
            job_execution = item[0]
            job_namespace = item[2]
            job_def =  item[1]
            
            tridggeres = json.loads ( job_execution.triggers)
            #self.log.error('tridggeres=%s' % tridggeres)
            params = json.loads ( job_execution.trig_parameters)
            for trig in tridggeres:
                self.log.error('trig=%s' % trig)
                
                update_query = session.query(model.job_def).\
                    filter(model.job_def.fk_type == model.job_namespace.id).\
                    filter(model.job_namespace.name == trig)
                self.log.error('count=%s' % update_query.count())
                for target in update_query:
                    fk_update = target.id
                    self.log.error('target.id=%s' % target.id)
                    new_cmdln = string.Template(target.cmdln_template).substitute(para)
                    self.log.info('new_cmdln=%s' % new_cmdln)
                    self.log.info('para=%s' % para)
                    newjob_execution = model.job_execution()
                    newjob_execution.fk_update = target.id
                    newjob_execution.name = ""
                    newjob_execution.created = datetime.datetime.now()
                    newjob_execution.expires = datetime.datetime.now()
                    newjob_execution.outputjson = None
                    newjob_execution.returncode = None
                    newjob_execution.uuid = str(uuid.uuid1())
                    newjob_execution.triggers = "[]"
                    newjob_execution.cmdln = new_cmdln
                    session.add(newjob_execution)
                    session.commit()

                
                
                
    def queue_dequeue(self, *args, **kwargs):
        self.log.debug('queue_dequeue')
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        find_job_def = session.query(model.job_execution,model.job_namespace).\
                filter(model.job_execution.expired == None).\
                filter(model.job_execution.returncode == None).\
                order_by(model.job_execution.created)
        #self.log.error('queue_dequeue=%s' % find_job_def.count())
        
        for item in find_job_def:
            job_execution = item[0]
            print job_execution.created
            job_namespace = item[1]
            new_job_runner = db_job_runner.job_runner()
            new_job_runner.session = session
            new_job_runner.job_class = job_namespace.name
            new_job_runner.outputjson = job_execution.outputjson
            new_job_runner.created = job_execution.created
            new_job_runner.expires = job_execution.expires
            new_job_runner.expired = job_execution.expires
            
            new_job_runner.run(session = session)
            job_execution.outputjson = new_job_runner.outputjson
            job_execution.finshed = datetime.datetime.now()
            job_execution.returncode = new_job_runner.returncode
            job_execution.cmdln = new_job_runner.cmdln
            job_execution.triggers = new_job_runner.triggers
            job_execution.trig_parameters = new_job_runner.trig_parameters
            
            session.add(job_execution)
            session.commit()
            return True
        

            
        return False
        
        
        

            
    def jobtype_available(self, *args, **kwargs):
        session = kwargs.get('jobtype_available', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("ddd")
            return
        outoup_set = set()
        job_types_query = session.query(model.job_namespace.name).all()
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
            self.log.warning("job_namespace_Add missing name")
            return
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.warning("unset self.session")
            return
        job_uuid = kwargs.get('uuid', None)
        if job_uuid  == None:
            ssss
            self.log.debug("No UUID specified")
            job_uuid = str(uuid.uuid4())
       
       
       
        find_create = session.query(model.job_state).\
                filter(model.job_state.name == "create")
        find_create_id = None
        find_create_count = find_create.count() 
        if find_create_count == 0:
            newjob_state = model.job_state()
            newjob_state.name = "create"
            session.add(newjob_state)
            session.commit()
         
        find_state_count = session.query(model.job_state).count() 
        
        if find_state_count == 0:
            self.log.error("Bad data base")
            return -2
        
        
        
        find_job_namespace = session.query(model.job_namespace).\
                filter(model.job_namespace.name == job_type)
       
        
        
        if find_job_namespace.count() == 0:
            newjob_namespace = model.job_namespace()
            newjob_namespace.name = job_type
            session.add(newjob_namespace)
            session.commit()
            find_job_namespace = session.query(model.job_namespace).\
                filter(model.job_namespace.name == job_type)
        
        ret_job_type = find_job_namespace.one()
        
        find_job_def = session.query(model.job_def).\
                filter(model.job_def.fk_type == ret_job_type.id).\
                filter(model.job_namespace.name == name).\
                filter(model.job_def.cmdln_template == cmdln_template).\
                filter(model.job_def.cmdln_paramters == cmdln_paramters)
                
        if find_job_def.count() == 0:
            newjob_def = model.job_def()
            newjob_def.fk_type = ret_job_type.id
            newjob_def.name = name
            newjob_def.cmdln_template = cmdln_template
            newjob_def.cmdln_paramters = cmdln_paramters
            newjob_def.uuid = job_uuid
            session.add(newjob_def)
            session.commit()
            find_job_def = session.query(model.job_def).\
                filter(model.job_def.fk_type == ret_job_type.id).\
                filter(model.job_namespace.name == name).\
                filter(model.job_def.cmdln_template == cmdln_template).\
                filter(model.job_def.cmdln_paramters == cmdln_paramters)
                
            
        if find_job_def.count() != 1:
            self.log.error("Some thign bad happened")

        ret_job_details = find_job_def.one()
        
        
        find_job_def = session.query(model.job_execution).\
                filter(model.job_execution.fk_update == model.job_def.id).\
                filter(model.job_def.fk_type == ret_job_type.id).\
                filter(model.job_namespace.name == name).\
                filter(model.job_def.cmdln_template == cmdln_template).\
                filter(model.job_def.cmdln_paramters == cmdln_paramters)
                        
        
        if find_job_def.count() == 0:
            newjob_execution = model.job_execution()
            newjob_execution.fk_update = ret_job_details
            newjob_execution.fk_state = 1
            newjob_execution.name = name
            newjob_execution.created = datetime.datetime.now()
            newjob_execution.expires = datetime.datetime.now()
            newjob_execution.outputjson = None
            newjob_execution.returncode = None
            newjob_execution.fk_update = ret_job_details.id
            newjob_execution.uuid = str(uuid.uuid1())
            newjob_execution.triggers = "[]"
            session.add(newjob_execution)
            session.commit()
def job_execution_Run(self,session):
    find_existing = session.query(model.job_namespace,model.job_def,model.job_execution).\
        filter(model.job_execution.expires < datetime.datetime.now()).\
        filter(model.job_def.fk_type == model.job_namespace.id).\
        filter(model.job_execution.fk_update == model.job_namespace.id)
    return find_existing
