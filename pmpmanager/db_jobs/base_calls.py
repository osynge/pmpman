import logging
import subprocess
import time
import pmpmanager.db_devices as model

def UpdateType_Add(*args, **kwargs):
    log = logging.getLogger("UpdateType_Add")
    name = kwargs.get('name', None)
    if name == None:
        log.warning("UpdateType_Add missing name")
        return
    session = kwargs.get('session', None)
    if session == None:
        log.warning("Update_Add missing name")
        return
    find_existing = session.query(model.UpdateType).\
            filter(model.UpdateType.name == name)
    if find_existing.count() >= 1:
        return
    newUpdateType = model.UpdateType()
    newUpdateType.name = name
    session.add(newUpdateType)
    session.commit()

def Update_Add(*args, **kwargs):
    log = logging.getLogger("Update_Add")
    update_type = kwargs.get('update_type', None)
    if update_type == None:
        log.warning("Update_Add missing update_type")
        return
    
    name = kwargs.get('name', None)
    if name == None:
        log.warning("Update_Add missing name")
        return
    session = kwargs.get('session', None)
    if session == None:
        log.warning("Update_Add missing name")
        return
    find_existing = session.query(model.UpdateInstance).\
            filter(model.UpdateType.name == update_type)
    if find_existing.count == 0:
        newUpdateType = model.UpdateType()
        newUpdateType.name = name
        session.add(newUpdateType)
        session.commit()
        session = self.SessionFactory()
        find_existing = session.query(model.UpdateType).\
            filter(model.UpdateType.name == name)
        log.warning( find_existing.one())

def runpreloadcommand(cmd,timeout):
    process = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    
    def execuet_cmdln(self, *args, **kwargs):
        cmd = kwargs.get('cmdln', 10)
        timeout = kwargs.get('timeout', 10)
        return runpreloadcommand(cmd,timeout)
    
    def save(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("session is None")
            return
        #for it in self.session.query()
        #self.log.error("self.job_class=%s" % self.job_class)
        #self.log.error("self.session=%s" % self.session)
        UpdateType_Add(session=self.session,
             name = self.job_class)
        Update_Add(session=self.session,
             update_type = self.job_class,
             name = self.job_class,
             cmdln_template = self.cmdln_template
             )
    def run(self, *args, **kwargs):
        pass
