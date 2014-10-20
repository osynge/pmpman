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


import db_jobs.lsblk_query as job_runner_lsblk_query
import db_jobs.lsblk_read as job_runner_lsblk_read

import db_jobs.udev_query as job_runner_udev_query
import db_jobs.udev_query as job_runner_udev_read
import db_jobs.udev_read as job_runner_udev_read
 
   


class job_runner(object):
    """Facade class for mulitple implementations of a job junner,
    Should be robust for setting the impleemntation or attributes
    in any order."""
    
    def __init__(self):
        self.log = logging.getLogger("job_runner_facade")
        self.job_classes = { 
            "kname_new" :  job_runner_udev_read,
            "udev_query" : job_runner_udev_query ,
            "lsblk" : job_runner_lsblk_query,
            "udev_read" : job_runner_udev_read,
            "lsblk_read" : job_runner_lsblk_read,
            }
        
    @Property
    def job_class():
        def fget(self):
            if hasattr(self, '_job_class'):
                return self._job_class
            else:
                return None

        def fset(self, name):
            if hasattr(self, '_job_class'):
                if name == self._job_class:
                    self.log.error("dont replay")
                    return
            self._job_class_name = name
            if not name in self.job_classes.keys():
                self.log.error("Cant set job class to=%s" % (name))
                self.log.info('Valid upload protocols are ["%s"]' % (self.job_classes.keys()))
                if hasattr(self, '_job_class'):
                    del (self._job_runnerImp)
                return
            
                
            tmpJobRnner = self.job_classes[name].job_runner()
            tmpJobRnner.job_class = name
            tmpJobRnner.session = self.session
            tmpJobRnner.cmdln = self.cmdln
            tmpJobRnner.returncode = self.returncode
            tmpJobRnner.outputjson = self.outputjson
            tmpJobRnner.created = self.created
            tmpJobRnner.expires = self.expires
            tmpJobRnner.expired = self.expired

            if hasattr(self, '_job_class'):
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
    
    
    
    def run(self, *args, **kwargs):
        if hasattr(self, '_job_runnerImp'):
            return self._job_runnerImp.run(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if hasattr(self, '_job_runnerImp'):
            return self._job_runnerImp.save()


        
    def restore(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        restor_details = None
        key = kwargs.get('key', None)
        if key != None:
            restor_details = session.query(model.UpdateType).\
                filter(model.UpdateType.name == name).one()
        if getdetails == None:
            pass
            
        
        
        
        
