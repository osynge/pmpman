import logging
import subprocess
import time
import pmpmanager.db_devices as model
import uuid

def Property(func):
    return property(**func())

def job_namespace_Add(*args, **kwargs):
    log = logging.getLogger("job_namespace_Add")
    name = kwargs.get('name', None)
    if name == None:
        log.warning("job_namespace_Add missing name")
        return
    session = kwargs.get('session', None)
    if session == None:
        log.warning("job_def_Add missing name")
        return
    find_existing = session.query(model.job_namespace).\
            filter(model.job_namespace.name == name)
    if find_existing.count() >= 1:
        return
    newjob_namespace = model.job_namespace()
    newjob_namespace.name = name
    session.add(newjob_namespace)
    session.commit()

def job_def_Add(*args, **kwargs):
    log = logging.getLogger("job_def_Add")
    update_type = kwargs.get('update_type', None)
    if update_type == None:
        log.warning("job_def_Add missing update_type")
        return
    
    name = kwargs.get('name', None)
    if name == None:
        log.warning("job_def_Add missing name")
        return
    session = kwargs.get('session', None)
    if session == None:
        log.warning("job_def_Add missing name")
        return
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
        log.warning( find_existing.one())



def store_sk_uuid_job_triggers(*args, **kwargs):
    log = logging.getLogger("store_sk_uuid_job_triggers")
    source = kwargs.get('source', None)
    if source == None:
        log.info("missing source")
        return
    dest = kwargs.get('dest', None)
    if dest == None:
        log.warning("missing dest")
        return
    
    sk_uuid = kwargs.get('sk_uuid', None)
    if sk_uuid == None:
        fdsdfdsf
        log.warning("missing sk_uuid")
        return
    session = kwargs.get('session', None)
    if session == None:
        log.warning("missing name")
        return
    find_existing = session.query(model.job_triggers,).\
            filter(model.job_triggers.source == source).\
            filter(model.job_triggers.dest == dest)
            
            
    if find_existing.count == 0:
        newjob_namespace = model.job_namespace()
        newjob_namespace.name = name
        session.add(newjob_namespace)
        session.commit()
        session = self.SessionFactory()
        find_existing = session.query(model.job_triggers,).\
            filter(model.job_namespace.name == source).\
            filter(model.name == source)
            
            
        log.warning( find_existing.one())



def runpreloadcommand(cmd,timeout):
    process = subprocess.Popen([str(cmd)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processRc = None
    handleprocess = True
    counter = 0
    stdout = ''
    stderr = ''
    while handleprocess:
        counter += 1
        time.sleep(1)
        cout,cerr = process.communicate()
        stdout += cout
        stderr += cerr
        process.poll()
        processRc = process.returncode
        if processRc != None:
            break
        if counter == timeout:
            os.kill(process.pid, signal.SIGQUIT)
        if counter > timeout:
            os.kill(process.pid, signal.SIGKILL)
            processRc = -9
            break
    return (processRc,stdout,stderr)

class job_runner():

    
    def store_job_triggers(self, *args, **kwargs):
        
        return store_sk_uuid_job_triggers(*args,**kwargs)
    
    
    def execuet_cmdln(self, *args, **kwargs):
        cmd = kwargs.get('cmdln', 10)
        timeout = kwargs.get('timeout', 10)
        return runpreloadcommand(cmd,timeout)
    
    def save(self, *args, **kwargs):
        print 
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("session is None")
            return
        #for it in self.session.query()
        #self.log.error("self.job_class=%s" % self.job_class)
        #self.log.error("self.session=%s" % self.session)
        job_namespace_Add(session=self.session,
             name = self.job_class)
             
        
        job_def_Add(session=self.session,
             update_type = self.job_class,
             name = self.job_class,
             cmdln_template = self.cmdln_template
             )
        self.store_job_triggers(session=self.session,
             update_type = self.job_class,
             name = self.job_class,
             cmdln_template = self.cmdln_template,
             source = "ssss",
             dest = "dddddd",
             sk_uuid = str(self.uuid_execution)
        )
        
        
        
    def run(self, *args, **kwargs):
        pass


    def load(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("No session set")
            return False

        uuid_def = kwargs.get('uuid_def', None)
        if uuid_def == None:
           uuid_def = self.uuid_def
        if uuid_def == None:
            self.log.error("No uuid_def set")
            return False
        
        uuid_execution = kwargs.get('uuid_execution', None)
        if uuid_execution == None:
           uuid_execution = self.uuid_execution
        if uuid_execution == None:
            self.log.error("No uuid_execution set")
            return False
        query_job_def = session.query(model.job_def).\
                filter(model.job_def.uuid == uuid_def)
        if query_job_def.count() == 0:
            self.log.error("failed to find uuid_def:%s" % (uuid_def))
            return False

        query_job_execution = session.query(model.job_execution).\
                filter(model.job_execution.uuid == uuid_execution)
        if query_job_execution.count() == 0:
            self.log.error("failed to find uuid_def:%s" % (uuid_execution))
            return False
        
        query_job_namespace = session.query(model.job_namespace).\
                filter(model.job_execution.uuid == uuid_execution).\
                filter(model.job_def.uuid == uuid_def).\
                filter(model.job_def.id == model.job_execution.fk_update).\
                filter(model.job_namespace.id == model.job_def.fk_type)
        if query_job_namespace.count() == 0:
            self.log.error("failed to find job_namespace:%s" % (uuid_execution))
            return False
        
        query_job_state = session.query(model.job_state).\
                filter(model.job_execution.uuid == uuid_execution).\
                filter(model.job_def.uuid == uuid_def).\
                filter(model.job_def.id == model.job_execution.fk_update).\
                filter(model.job_state.id == model.job_def.fk_type)
        if query_job_state.count() == 0:
            self.log.error("failed to find job_state:%s" % (uuid_execution))
            return False
        
        job_state= query_job_state.one()
        self.state = job_state.name
        
        job_namespace = query_job_namespace.one()
        
        job_def = query_job_def.one()
        self.cmdln_template = job_def.cmdln_template
        self.cmdln_paramters= job_def.cmdln_paramters
        self.reocuring = job_def.reocuring
        
        
        job_execution = query_job_execution.one()
        
        self.cmdln = job_execution.cmdln
        self.returncode = job_execution.cmdln
        self.outputjson = job_execution.outputjson
        self.created = job_execution.created
        self.expires = job_execution.expires
        self.expired = job_execution.expired
        
        return True

    @Property
    def cmdln():
        doc = "Remote upload prefix"

        def fget(self):
            return self._session

        def fset(self, value):
            self._session = value
            
        def fdel(self):
            del self._session
        return locals()
    
    @Property
    def arguments():
        doc = "Remote upload prefix"

        def fget(self):
            return self._session

        def fset(self, value):
            self._session = value
            
        def fdel(self):
            del self._session
        return locals()
    
