


import logging
    
import json

from base_calls import job_runner as bass_job_runner


def Property(func):
    return property(**func())
    

class job_runner(bass_job_runner):
    def __init__(self):
        self.remotePrefix = None
        self.log = logging.getLogger("job_runner.udev_read")
        self.cmdln_template = None


    @Property
    def session():
        doc = "Remote upload prefix"

        def fget(self):
            return self._session

        def fset(self, value):
            self._session = value
            
        def fdel(self):
            del self._session
        return locals()
    
    
    def run(self, *args, **kwargs):
        self.log.debug("self.job_class=%s" % (self.job_class))
        self.triggers = json.dumps([],sort_keys=True, indent=4)
        self.trig_parameters = json.dumps([],sort_keys=True, indent=4)
        session = kwargs.get('session', None)
        if session == None:
            log.warning("Update_Add missing name")
            return
        session.query()

        
        
