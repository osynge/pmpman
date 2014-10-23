
import pmpmanager.db_devices as model

import logging
    
import json

from base_calls import job_exec as bass_job_exec



class job_exec(bass_job_exec):
    def __init__(self):
        self.remotePrefix = None
        self.log = logging.getLogger("job_exec.udev_read")
        self.cmdln_template = None

    def run(self, *args, **kwargs):
        self.log.debug("self.job_class=%s" % (self.job_class))
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("No session set")
            return False
        inputjson = kwargs.get('inputjson', None)
        if inputjson == None:
            inputjson = self.inputjson
        if inputjson == None:
            self.log.error("No inputjson set")
            return False

        output = {}
        # Query the database
        names = []
        instance_query = session.query(model.Block).all()
        for item in instance_query:
            print item.devName
            print item.devPath
            

