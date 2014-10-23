import logging

def Property(func):
    return property(**func())

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg


import db_devices as model


import job_exec

from sqlalchemy.orm import aliased

from uuid import uuid1 as uuidgen

class job_template(object):
    """Facade class for mulitple implementations of a job junner,
    Should be robust for setting the impleemntation or attributes
    in any order."""

    def __init__(self):
        self.log = logging.getLogger("job_template")
        
        self.subscribe_list = set([])
        self.publish_list = set([])
    @Property
    def job_class():
        doc = "Remote upload prefix"

        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'job_class'):
                        return self._job_runnerImp.job_class
                    else:
                        return None
            if hasattr(self, '_job_class'):
                return self._job_class

        def fset(self, value):
            self._job_class = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.job_class != value:
                        self._job_runnerImp.job_class = value
        def fdel(self):
            del self._job_class
        return locals()
    @Property
    def session():
        doc = "Remote upload prefix"

        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'session'):
                        return self._job_runnerImp.session
                    else:
                        return None
            if hasattr(self, '_session'):
                return self._session

        def fset(self, value):
            self._session = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.session != value:
                        self._job_runnerImp.session = value
        def fdel(self):
            del self._session
        return locals()
   
    @Property
    def created():
        doc = "Remote upload prefix"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'created'):
                        return self._job_runnerImp.created
                    else:
                        return None
            if hasattr(self, '_created'):
                return self._created

        def fset(self, value):
            self._created = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.created != value:
                        self._job_runnerImp.created = value
        def fdel(self):
            del self._created
        return locals()

    @Property
    def expires():
        doc = "Remote upload prefix"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'expires'):
                        return self._job_runnerImp.expires
                    else:
                        return None
            if hasattr(self, '_expires'):
                return self._expires

        def fset(self, value):
            self._expires = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.expires != value:
                        self._job_runnerImp.expires = value
        def fdel(self):
            del self._expires
        return locals()


    @Property
    def expired():
        doc = "Remote upload prefix"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'expired'):
                        return self._job_runnerImp.expired
                    else:
                        return None
            if hasattr(self, '_expired'):
                return self._expired

        def fset(self, value):
            self._expired = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.expired != value:
                        self._job_runnerImp.expired = value
        def fdel(self):
            del self._expired
        return locals()

    @Property
    def uuid():
        doc = "Get a persistent UUID for this operation"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'uuid'):
                        return self._job_runnerImp.uuid
                    else:
                        return None
            if hasattr(self, '_uuid'):
                return self._uuid

        def fset(self, value):
            self._uuid = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.uuid != value:
                        self._job_runnerImp.uuid = value
        def fdel(self):
            del self._uuid
        return locals()


    @Property
    def cmdln_template():
        doc = "Get a persistent UUID for this operation"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'cmdln_template'):
                        return self._job_runnerImp.cmdln_template
                    else:
                        return None
            if hasattr(self, '_cmdln_template'):
                return self._cmdln_template

        def fset(self, value):
            self._cmdln_template = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.cmdln_template != value:
                        self._job_runnerImp.cmdln_template = value
        def fdel(self):
            del self._cmdln_template
        return locals()

    @Property
    def cmdln_paramters():
        doc = "Get a persistent UUID for this operation"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'cmdln_paramters'):
                        return self._job_runnerImp.cmdln_paramters
                    else:
                        return None
            if hasattr(self, '_cmdln_paramters'):
                return self._cmdln_paramters

        def fset(self, value):
            self._cmdln_paramters = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.cmdln_paramters != value:
                        self._job_runnerImp.cmdln_paramters = value
        def fdel(self):
            del self._cmdln_paramters
        return locals()

    @Property
    def reocuring():
        doc = "Get a persistent UUID for this operation"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'reocuring'):
                        return self._job_runnerImp.reocuring
                    else:
                        return None
            if hasattr(self, '_reocuring'):
                return self._reocuring

        def fset(self, value):
            self._reocuring = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.reocuring != value:
                        self._job_runnerImp.reocuring = value
        def fdel(self):
            del self._reocuring
        return locals()

  
    
    @Property
    def uuid_req():
        doc = "Get a persistent UUID for this operation"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'uuid_req'):
                        return self._job_runnerImp.uuid_req
                    else:
                        return None
            if hasattr(self, '_uuid_req'):
                return self._uuid_req

        def fset(self, value):
            if value == None:
                value = set([])
            self._uuid_req = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.uuid_req != value:
                        self._job_runnerImp.uuid_req = value
        def fdel(self):
            del self._uuid_req
        return locals()
    
    @Property
    def subscribe_list():
        doc = "Get a persistent UUID for this operation"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'subscribe_list'):
                        return self._job_runnerImp.subscribe_list
                    else:
                        return None
            if hasattr(self, '_subscribe_list'):
                return self._subscribe_list

        def fset(self, value):
            if value == None:
                raise InputError("None is invalid")


            self._subscribe_list = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.subscribe_list != value:
                        self._job_runnerImp.subscribe_list = value
        def fdel(self):
            del self._subscribe_list
        return locals()

    @Property
    def publish_list():
        doc = "Get a persistent UUID for this operation"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'publish_list'):
                        return self._job_runnerImp.publish_list
                    else:
                        return None
            if hasattr(self, '_publish_list'):
                return self._publish_list

        def fset(self, value):
            if value == None:
                value = set([])
            self._publish_list = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.publish_list != value:
                        self._job_runnerImp.publish_list = value
        def fdel(self):
            del self._publish_list
        return locals()


    
    def subscribe_add(self, subscribe_uuid, **kwargs):
        old_subscribe = self.subscribe_list
        old_subscribe.add(subscribe_uuid)
        self.subscribe_list = old_subscribe

    def subscribe_del(self, subscribe_uuid, **kwargs):
        old_subscribe = self.subscribe_list
        old_subscribe.delete(subscribe_uuid)
        self.subscribe_list = old_subscribe

    def enqueue(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("enqueue:No session set")
            raise InputError("No session set")
        uuid_job = kwargs.get('uuid_job', None)
        if uuid_job == None:
            self.log.error("enqueue:No uuid_job set")
            raise InputError("No uuid_job set")
        reocuring = kwargs.get('reocuring', None)
        if reocuring == None:
            self.log.error("enqueue:No reocuring set")
            raise InputError("No reocuring set")
        uuid_job = kwargs.get('uuid_job', None)
        if uuid_job == None:
            self.log.error("enqueue:No uuid_job set")
            raise InputError("No uuid_job set")
        
        uuid_job = kwargs.get('uuid_job', None)
        if uuid_job == None:
            self.log.error("enqueue:No uuid_job set")
            raise InputError("No uuid_job set")
        
        job_class = kwargs.get('job_class', None)
        if job_class == None:
            self.log.error("enqueue:No job_class set")
            raise InputError("No job_class set")
        
        cmdln_paramters = kwargs.get('cmdln_paramters', None)
        if cmdln_paramters == None:
            self.log.error("enqueue:No cmdln_paramters set")
            raise InputError("No cmdln_paramters set")
        
        uuid_job_def = kwargs.get('uuid_job_def', None)
        if uuid_job_def == None:
            self.log.error("enqueue:No uuid_job_def set")
            raise InputError("No uuid_job_def set")
        
        
        
        if uuid_job == None:
            uuid_job = str(uuidgen)
        enqueue_job_runner = job_exec.job_exec()
        if self.job_class != None:
            enqueue_job_runner.job_class = self.job_class
        enqueue_job_runner.uuid_execution = uuid_job
        enqueue_job_runner.reocuring = self.reocuring
        enqueue_job_runner.cmdln_template = self.cmdln_template
        enqueue_job_runner.cmdln_paramters = self.cmdln_paramters
        # Now save queued request
        rc = enqueue_job_runner.save(session = session,
            uuid_tempate=uuid_job,
            cmdln_paramters=cmdln_paramters,
            uuid_job_def=uuid_job_def,
            )
        session.commit()
        return True
        


    def run(self, *args, **kwargs):
        if hasattr(self, '_job_runnerImp'):
            return self._job_runnerImp.run(*args, **kwargs)

    def queue_count(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            raise InputError("No session set")
        
        workuuid = kwargs.get('uuid', None)
        if workuuid == None:
            workuuid = self.uuid
        if workuuid == None:
            raise InputError("No workuuid set")
        
        query_job_namespace = session.query(model.job_execution).\
                filter(model.job_execution.fk_update == model.job_def.id).\
                filter(model.job_execution.uuid_job_execution == workuuid)
        return query_job_namespace.count()
        
        
        
    def save(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            raise InputError("No session set")

        uuid_save = kwargs.get('uuid', None)
        if uuid_save == None:
           uuid_save = self.uuid
        if uuid_save == None:
            raise InputError("No uuid set")
        
        cmdln_template = kwargs.get('cmdln_template', None)
        if cmdln_template == None:
           cmdln_template = self.cmdln_template
        if cmdln_template == None:
            raise InputError("No cmdln_template set")
        
        
        
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            sdsdfsdfs
            self.log.error("No session set")
            return False

        job_class = kwargs.get('job_class', None)
        if job_class == None:
           job_class = self.job_class
        if job_class == None:
            self.log.error("No job_class set")
            return False
        
        # Finished input validation

        query_job_namespace = session.query(model.job_namespace).\
                filter(model.job_namespace.name == job_class)
        if query_job_namespace.count() == 0:
            job_namespace = model.job_namespace()
            job_namespace.name = job_class
            session.add(job_namespace)
            session.commit()
            query_job_namespace = session.query(model.job_namespace).\
                filter(model.job_namespace.name == job_class)

        job_namespace = query_job_namespace.one()

        query_job_def = session.query(model.job_def).\
                filter(model.job_def.uuid_job_def == uuid_save)

        if query_job_def.count() == 0:
            job_def = model.job_def()
            job_def.fk_type = job_namespace.id
            job_def.cmdln_template = self.cmdln_template
            job_def.cmdln_paramters = self.cmdln_paramters
            job_def.reocuring = self.reocuring
            job_def.uuid_job_def = uuid_save
            session.add(job_def)
            session.commit()
            query_job_def = session.query(model.job_def).\
                filter(model.job_def.uuid_job_def == uuid_save)

        job_def = query_job_def.one()
        job_def.cmdln_template = self.cmdln_template
        job_def.cmdln_paramters = self.cmdln_paramters
        job_def.reocuring = self.reocuring
        job_def.fk_type = job_namespace.id
        session.add(job_def)
        session.commit()


        # Define sets of source and dest
        subscribers_found = set()
        publishers_found = set()

        source_job = aliased(model.job_def, name='source_job')
        dest_job = aliased(model.job_def, name='dest_job')

        query_subscribers = session.query(dest_job).\
                filter(source_job.uuid_job_def == uuid_save).\
                filter(model.job_triggers.dest == dest_job.id).\
                filter(model.job_triggers.source == source_job.id)

        for item in query_subscribers:
            subscribers_found.add(item.uuid_job_def)
        
        
        query_publishers = session.query(source_job.uuid_job_def).\
                filter(dest_job.uuid_job_def == uuid_save).\
                filter(model.job_triggers.dest == dest_job.id).\
                filter(model.job_triggers.source == source_job.id)

        for item in query_publishers:
            publishers_found.add(item.uuid_job_def)


        subscribers_missing = self.subscribe_list.difference(subscribers_found)
        publishers_missing = self.publish_list.difference(subscribers_found)
        subscribers_extra = subscribers_found.difference(self.subscribe_list)
        publishers_extra= subscribers_found.difference(self.publish_list)

        self.log.debug("subscribers_missing=%s" % (subscribers_missing))
        for item in subscribers_missing:
            query_new = session.query(model.job_def).\
                filter(model.job_def.uuid_job_def == item)
            for item in query_new:
                newtrigger = model.job_triggers()
                newtrigger.source = item.id
                newtrigger.dest = job_def.id
                newtrigger.sk_uuid = str(uuidgen())
                session.add(newtrigger)
                session.commit()

        self.log.debug("publishers_missing=%s" % (publishers_missing))
        for item in publishers_missing:
            query_new = session.query(model.job_def).\
                filter(model.job_def.uuid_job_def == item)
            for item in query_new:
                newtrigger = model.job_triggers()
                newtrigger.source = job_def.id
                newtrigger.sk_uuid = str(uuidgen())
                newtrigger.dest = item.id
                session.add(newtrigger)
                session.commit()
        self.log.debug("subscribers_extra=%s" % (subscribers_extra))
        self.log.debug("publishers_extra=%s" % (publishers_extra))


            
        
    def load(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            raise InputError("No session set")

        uuid = kwargs.get('uuid', None)
        if uuid == None:
           uuid = self.uuid
        if uuid == None:
            raise InputError("No uuid set")
        
        
        query_job_def = session.query(model.job_def).\
                filter(model.job_def.uuid_job_def == uuid)
        if query_job_def.count() == 0:
            self.log.error("failed to find uuid_def:%s" % (uuid))
            raise InputError("Invalid uuid set")

        query_job_namespace = session.query(model.job_namespace).\
                filter(model.job_def.uuid_job_def == uuid).\
                filter(model.job_namespace.id == model.job_def.fk_type)

        if query_job_namespace.count() == 0:
            self.log.error("failed to find job_namespace:%s" % (uuid_execution))
            raise InputError("failed to find job_namespace")
        job_namespace = query_job_namespace.one()
        job_def = query_job_def.one()
        
        self.uuid_def = job_def.uuid_job_def
        self.job_class = job_namespace.name


        self.cmdln_template = job_def.cmdln_template
        self.cmdln_paramters= job_def.cmdln_paramters
        self.reocuring = job_def.reocuring

        set_subscribers = set()
        query_subscribers = session.query(model.job_def).\
                filter(model.job_def.uuid_job_def == uuid).\
                filter(model.job_triggers.source == model.job_def.id)
        for item in query_subscribers:
            set_subscribers.add(str(item.uuid_job_def))
        self.subscribe_list = set(set_subscribers)
        
        set_publishers = set()
        query_publishers = session.query(model.job_def).\
                filter(model.job_def.uuid_job_def == uuid).\
                filter(model.job_triggers.dest == model.job_def.id)
        for item in query_publishers:
            set_publishers.add(str(item.uuid_job_def))
        self.publish_list = set(set_publishers)
        
        
        
    def show(self):

        output = {
            "uuid_req" : self.uuid_req,
            "publish_list" : self.publish_list,
            "subscribe_list" : self.subscribe_list,
            "reocuring" : self.reocuring,
            "cmdln_paramters" : self.cmdln_paramters,
            "cmdln_template" : self.cmdln_template,
            "uuid" : self.uuid,
            "expired" : self.expired,
            "expires" : self.expires,
            "created" : self.created,
            "job_class" : self.job_class
        }
        return output

class job_manage(object):
    def __init__(self):
        self.log = logging.getLogger("job_manage")
        self.subscribe_list = set([])
        self.publish_list = set([])
    
    
    def list_job_class(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("load:No session set")
            return False
        output = None
        query_job_execution = session.query(model.job_namespace)
        output = []
        for query_job_execution in query_job_execution:
            
            output.append(query_job_execution.name)
        return output

    def list_job_def(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("load:No session set")
            return False
        output = None
        query_job_execution = session.query(model.job_def)
        output = []
        for query_job_execution in query_job_execution:
            
            output.append(query_job_execution.uuid_job_def)
        return output
    
    
    def list_job_exec(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("load:No session set")
            return False
        output = None
        
        #query_job_state = session.query(model.job_execution,model.job_def,model.job_state,model.job_class).\
        #        filter(model.job_execution.uuid == uuid_execution).\
        #        filter(model.job_def.uuid == uuid_def).\
        #        filter(model.job_def.id == model.job_execution.fk_update).\
        #        filter(model.job_state.id == model.job_execution.fk_state).\
        #        filter(model.job_class.id == model.job_def.fk_type
        query_job_execution = session.query(model.job_execution)
        output = []
        for query_job_execution in query_job_execution:
            
            output.append(query_job_execution.uuid)
        return output

    def show_job_def(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("enqueue:No session set")
            return False
        job_def_uuid = kwargs.get('uuid', None)
        if job_def_uuid == None:
            self.log.error("show_job_def:No uuid set")
            return False
        
        
        
        
        query_job_execution = session.query(model.job_def).\
            filter(model.job_def.uuid == job_def_uuid)  
            
        output = []
        for query_job_execution in query_job_execution:
            job_tmp = job_template()
            job_tmp.session = session
            job_tmp.uuid = query_job_execution.uuid
            job_tmp.load(session = session)
            output.append(job_tmp.show())
        return output
    
    def get_job_def(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("enqueue:No session set")
            raise InputError("No session set")
        
        
        job_def_uuid_alt_01 = kwargs.get('uuid', None)
        job_def_uuid_alt_02 = kwargs.get('uuid_job_def', None)
        job_def_uuid = job_def_uuid_alt_01
        if job_def_uuid_alt_02 != None:
            job_def_uuid = job_def_uuid_alt_02
        
        if job_def_uuid == None:
            raise InputError("show_job_def:No uuid_job_def set")
        job_tmp = job_template()
        job_tmp.session = session
        job_tmp.uuid = job_def_uuid
        job_tmp.load(session = session)   
        return job_tmp


    def create_job_def(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("No session set")
            raise InputError("No session set")
            
            
        
        job_def_uuid = kwargs.get('uuid', None)
        if job_def_uuid == None:
            raise InputError("No uuid set")
        job_class = kwargs.get('job_class', None)
        if job_class == None:
            raise InputError("No job_class set")
        
        
        cmdln_template = kwargs.get('cmdln_template', None)
        if cmdln_template == None:
            raise InputError("No cmdln_template set")
        reocuring = kwargs.get('reocuring', None)
        if reocuring == None:
            raise InputError("No reocuring set")
        
        
        query_job_class = session.query(model.job_namespace).\
            filter(model.job_namespace.name == job_class).\
            count()
        if query_job_class == 0:
            raise InputError("Invalid job_class set")
        
        query_job_class = session.query(model.job_def).\
            filter(model.job_def.uuid_job_def == job_def_uuid).\
            count()
        if query_job_class != 0:
            return True 
        
        job_tmp = job_template()
        job_tmp.session = session
        job_tmp.uuid = job_def_uuid
        job_tmp.job_class = job_class
        job_tmp.cmdln_template = cmdln_template
        job_tmp.reocuring = reocuring
        job_tmp.save(session = session)   
        return True
    def create_job_class(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("No session set")
            return False
            
        name = kwargs.get('name', None)
        if name == None:
            raise InputError("No name set")
        
            
        
        output = None
        query_job_execution = session.query(model.job_namespace).\
            filter(model.job_namespace.name == name).count()
        if 0 == query_job_execution:
            newNamspeace = model.job_namespace()
            newNamspeace.name = name
            session.add(newNamspeace)
            session.commit()
        return True
