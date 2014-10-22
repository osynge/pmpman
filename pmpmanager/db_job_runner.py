import logging
import uuid

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


import db_jobs.lsblk_query as job_runner_lsblk_query
import db_jobs.lsblk_read as job_runner_lsblk_read

import db_jobs.udev_query as job_runner_udev_query
import db_jobs.udev_read as job_runner_udev_read
import db_jobs.no_ops as job_runner_no_ops

import db_devices as model





class job_runner(object):
    """Facade class for mulitple implementations of a job junner,
    Should be robust for setting the impleemntation or attributes
    in any order."""

    def __init__(self):
        self.log = logging.getLogger("job_runner_facade")
        self.job_classes = {
            "no_ops" : job_runner_no_ops,
            "kname_new" :  job_runner_udev_read,
            "udev_query" : job_runner_udev_query ,
            "lsblk_query" : job_runner_lsblk_query,
            "lsblk" : job_runner_lsblk_query,
            "udev_read" : job_runner_udev_read,
            "lsblk_read" : job_runner_lsblk_read,
            }
        self.subscribe_list = set([])
        self.publish_list = set([])

    @Property
    def job_class():
        def fget(self):
            if hasattr(self, '_job_class'):
                return self._job_class
            else:
                return None

        def fset(self, name):
            #if hasattr(self, '_job_class'):
            #    if name == self._job_class:
            #        self.log.debug("dont replay")
            #        return
            
            
            if name == None:

                raise InputError("None is an invalid value")
            try:
                self._job_class = name
            except pmpmanager.db_job_runner.InputError, E:
                print E.msg
                pass
            

                
            self.log.debug("set job_class:'%s'" % (name))
            if name == None:
                raise InputError("Cant be set to None")

            if not name in self.job_classes.keys():
                self.log.error("Failed seting job_class to=%s" % (name))
                self.log.debug('Valid job_class are "%s"' % (self.job_classes.keys()))
                self.log.info('Defaulting "job_class" value: "no_ops"')
                msg = str("Cant be set to:%s" % (name))
                raise InputError(msg)


            
            tmpJobRnner = self.job_classes[name].job_runner()
            tmpJobRnner.job_class = name
            tmpJobRnner.session = self.session
            tmpJobRnner.cmdln = self.cmdln
            tmpJobRnner.returncode = self.returncode
            tmpJobRnner.outputjson = self.outputjson
            tmpJobRnner.created = self.created
            tmpJobRnner.expires = self.expires
            tmpJobRnner.expired = self.expired
            tmpJobRnner.uuid_execution = self.uuid_execution
            tmpJobRnner.uuid_def = self.uuid_def
            tmpJobRnner.state = self.state
            tmpJobRnner.cmdln_template = self.cmdln_template
            tmpJobRnner.cmdln_paramters= self.cmdln_paramters
            tmpJobRnner.reocuring = self.reocuring
            tmpJobRnner.subscribe_list = self.subscribe_list
            tmpJobRnner.publish_list = self.publish_list

            if hasattr(self, '_job_runnerImp'):
                del (self._job_runnerImp)
            self._job_runnerImp = tmpJobRnner


        def fdel(self):
            del self._uploader
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
    def cmdln():
        doc = "Remote upload prefix"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'cmdln'):
                        return self._job_runnerImp.cmdln
                    else:
                        return None
            if hasattr(self, '_cmdln'):
                return self._cmdln

        def fset(self, value):
            self._cmdln = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.cmdln != value:
                        self._job_runnerImp.cmdln = value
        def fdel(self):
            del self._cmdln
        return locals()
    @Property
    def returncode():
        doc = "Remote upload prefix"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'returncode'):
                        return self._job_runnerImp.returncode
                    else:
                        return None
            if hasattr(self, '_returncode'):
                return self._returncode

        def fset(self, value):
            self._returncode = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.returncode != value:
                        self._job_runnerImp.returncode = value
        def fdel(self):
            del self._returncode
        return locals()
    @Property
    def outputjson():
        doc = "Remote upload prefix"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'outputjson'):
                        return self._job_runnerImp.outputjson
                    else:
                        return None
            if hasattr(self, '_outputjson'):
                return self._outputjson

        def fset(self, value):
            self._outputjson = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.outputjson != value:
                        self._job_runnerImp.outputjson = value
        def fdel(self):
            del self._outputjson
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
    def triggers():
        doc = "Remote upload prefix"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'triggers'):
                        return self._job_runnerImp.triggers
                    else:
                        return None
            if hasattr(self, '_triggers'):
                return self._triggers

        def fset(self, value):
            self._triggers = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.triggers != value:
                        self._job_runnerImp.triggers = value
        def fdel(self):
            del self._triggers
        return locals()


    @Property
    def trig_parameters():
        doc = "Remote upload prefix"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'trig_parameters'):
                        return self._job_runnerImp.trig_parameters
                    else:
                        return None
            if hasattr(self, '_trig_parameters'):
                return self._trig_parameters

        def fset(self, value):
            self._trig_parameters = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.trig_parameters != value:
                        self._job_runnerImp.trig_parameters = value
        def fdel(self):
            del self._trig_parameters
        return locals()

    @Property
    def uuid_execution():
        doc = "Get a persistent UUID for this operation"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'uuid_execution'):
                        return self._job_runnerImp.uuid_execution
                    else:
                        return None
            if hasattr(self, '_uuid_execution'):
                return self._uuid_execution

        def fset(self, value):
            self._uuid_execution = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.uuid_execution != value:
                        self._job_runnerImp.uuid_execution = value
        def fdel(self):
            del self._uuid_execution
        return locals()

    @Property
    def uuid_def():
        doc = "Get a persistent UUID for this operation"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'uuid_def'):
                        return self._job_runnerImp.uuid_def
                    else:
                        return None
            if hasattr(self, '_uuid_def'):
                return self._uuid_def

        def fset(self, value):
            self._uuid_def = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.uuid_def != value:
                        self._job_runnerImp.uuid_def = value
        def fdel(self):
            del self._uuid_def
        return locals()

    @Property
    def state():
        doc = "Get a persistent UUID for this operation"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'state'):
                        return self._job_runnerImp.state
                    else:
                        return None
            if hasattr(self, '_state'):
                return self._state

        def fset(self, value):
            self._state = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.state != value:
                        self._job_runnerImp.state = value
        def fdel(self):
            del self._state
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
            return False
        uuid_job = kwargs.get('uuid', None)
        if uuid_job == None:
            uuid_job = str(uuid.uuid1())
        enqueue_job_runner = job_runner()
        if self.job_class != None:
            enqueue_job_runner.job_class = self.job_class
        enqueue_job_runner.uuid_execution = uuid_job
        enqueue_job_runner.uuid_def = self.uuid_def
        enqueue_job_runner.reocuring = self.reocuring
        enqueue_job_runner.cmdln_template = self.cmdln_template
        enqueue_job_runner.cmdln_paramters = self.cmdln_paramters


        # Now save queued request
        enqueue_job_runner.save(session = session)
        session.commit()

        return True

    def run(self, *args, **kwargs):
        if hasattr(self, '_job_runnerImp'):
            return self._job_runnerImp.run(*args, **kwargs)

    def save(self, *args, **kwargs):
        if hasattr(self, '_job_runnerImp'):
            return self._job_runnerImp.save(*args, **kwargs)



    def load(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("load:No session set")
            return False

        uuid_def = kwargs.get('uuid_def', None)
        if uuid_def == None:
           uuid_def = self.uuid_def
        if uuid_def == None:
            self.log.error("No uuid_def set")
            return False
        
        uuid_req = kwargs.get('uuid_req', None)
        if uuid_req == None:
           uuid_req = self.uuid_req
           
        if uuid_req == None:
            self.log.error("No uuid_req set")
            raise InputError("No uuid_req set")
            
        uuid_execution = kwargs.get('uuid_execution', None)
        if uuid_execution == None:
           uuid_execution = self.uuid_execution
        if uuid_execution == None:
            raise InputError("No uuid_execution set")
        query_job_def = session.query(model.job_def).\
                filter(model.job_def.uuid == uuid_def)
        if query_job_def.count() == 0:
            self.log.error("failed to find uuid_def:%s" % (uuid_def))
            return False

        query_job_execution = session.query(model.job_execution).\
                filter(model.job_execution.uuid == uuid_execution)
        if query_job_execution.count() == 0:
            msg = "failed to find uuid_def:%s" % (uuid_execution)
            self.log.error(msg)
            raise InputError(msg)

        query_job_namespace = session.query(model.job_namespace).\
                filter(model.job_execution.uuid == uuid_execution).\
                filter(model.job_def.uuid == uuid_def).\
                filter(model.job_def.id == model.job_execution.fk_update).\
                filter(model.job_namespace.id == model.job_def.fk_type)
        if query_job_namespace.count() == 0:
            self.log.error("failed to find job_namespace:%s" % (uuid_execution))
            return False
        job_namespace = query_job_namespace.one()

        job_def = query_job_def.one()
        job_execution = query_job_execution.one()

        self.job_class = job_namespace.name
        if hasattr(self, '_job_runnerImp'):
            return self._job_runnerImp.load(*args, **kwargs)

