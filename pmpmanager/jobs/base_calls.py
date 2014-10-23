import logging
import subprocess
import time
import pmpmanager.db_devices as model
import uuid
from sqlalchemy.orm import aliased

def Property(func):
    return property(**func())




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

class job_exec(object):


    def store_job_triggers(self, *args, **kwargs):

        return store_sk_uuid_job_triggers(*args,**kwargs)


    def execuet_cmdln(self, *args, **kwargs):
        cmd = kwargs.get('cmdln', 10)
        timeout = kwargs.get('timeout', 10)
        return runpreloadcommand(cmd,timeout)

    def save(self, *args, **kwargs):
        #self.log.debug("save")
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
            
        uuid_tempate = kwargs.get('uuid_tempate', None)
        if uuid_tempate == None:
           uuid_tempate = self.uuid_tempate
        if uuid_tempate == None:
            self.log.error("No uuid_tempate set")
            return False
        
        
        # Now the ones we dont need
        uuid_execution = kwargs.get('uuid_execution', None)
        if uuid_execution == None:
           uuid_execution = self.uuid_execution
        if uuid_execution == None:
            self.log.error("No uuid_execution set")
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
                filter(model.job_execution.uuid == uuid_tempate)

        if query_job_def.count() == 0:
            self.log.error("Not found")
            job_def = model.job_def()
            
            job_def.fk_type = job_namespace.id
            job_def.cmdln_template = self.cmdln_template
            job_def.uuid = uuid_execution
            session.add(job_def)
            session.commit()
            query_job_def = session.query(model.job_def).\
                filter(model.job_execution.uuid == uuid_execution)
            self.log.error("ssssssssssstgggsssSSS")
        if (query_job_def.count() == 0):
            self.log.error("ssssssssssssssSSS")
            
        job_def = query_job_def.one()
        job_def.cmdln_template = self.cmdln_template
        job_def.cmdln_paramters = self.cmdln_paramters

        job_def.fk_type = job_namespace.id
        session.add(job_def)
        session.commit()



        subscribers_found = set()
        publishers_found = set()

        source_job = aliased(model.job_def, name='source_job')
        dest_job = aliased(model.job_def, name='dest_job')

        query_subscribers = session.query(dest_job).\
                filter(source_job.uuid == uuid_def).\
                filter(model.job_triggers.dest == dest_job.id).\
                filter(model.job_triggers.source == source_job.id)

        for item in query_subscribers:
            subscribers_found.add(item.uuid)
        query_publishers = session.query(source_job.uuid).\
                filter(dest_job.uuid == uuid_def).\
                filter(model.job_triggers.dest == dest_job.id).\
                filter(model.job_triggers.source == source_job.id)

        for item in query_publishers:
            publishers_found.add(item.uuid)


        subscribers_missing = self.subscribe_list.difference(subscribers_found)
        publishers_missing = self.publish_list.difference(subscribers_found)
        subscribers_extra = subscribers_found.difference(self.subscribe_list)
        publishers_extra= subscribers_found.difference(self.publish_list)

        self.log.debug("subscribers_missing=%s" % (subscribers_missing))
        for item in subscribers_missing:
            query_new = session.query(model.job_def).\
                filter(model.job_def.uuid == item)
            for item in query_new:
                newtrigger = model.job_triggers()
                newtrigger.source = item.id
                newtrigger.dest = job_def.id
                newtrigger.sk_uuid = str(uuid.uuid1())
                session.add(newtrigger)
                session.commit()

        self.log.debug("publishers_missing=%s" % (publishers_missing))
        for item in subscribers_missing:
            query_new = session.query(model.job_def).\
                filter(model.job_def.uuid == item)
            for item in query_new:
                newtrigger = model.job_triggers()
                newtrigger.source = job_def.id
                newtrigger.sk_uuid = str(uuid.uuid1())
                newtrigger.dest = item.id
                session.add(newtrigger)
                session.commit()
        self.log.debug("subscribers_extra=%s" % (subscribers_extra))
        self.log.debug("publishers_extra=%s" % (publishers_extra))



        need_uuid_execution = False
        if self.state != None:
            need_uuid_execution = True
        if not need_uuid_execution:
            self.log.debug("No execution details set.")
            return True
        if uuid_execution == None:
            self.log.error("No uuid_execution set")
            return False


        # Query remaining details

        query_job_state = session.query(model.job_state).\
                filter(model.job_execution.uuid == uuid_execution).\
                filter(model.job_def.uuid == uuid_def).\
                filter(model.job_def.id == model.job_execution.fk_update).\
                filter(model.job_state.id == model.job_def.fk_type)
        if query_job_state.count() == 0:
            self.log.error("failed to find job_state:%s" % (uuid_execution))
            return False


        query_job_execution = session.query(model.job_execution).\
                filter(model.job_execution.uuid == uuid_execution)
        if query_job_execution.count() == 0:
            self.log.error("failed to find uuid_def:%s" % (uuid_execution))
            return False


        job_state= query_job_state.one()
        if self.state != job_state.name:
            # We have to save the state
            available_state = session.query(model.job_state).\
                filter(model.job_state.name == self.state).\
                count()
            if available_state == 0:
                log.critical("Invalid State:" % self.state)
                return False
            newState = available_state.one()
            query_job_execution.fk_state.id()
            session.add(query_job_execution)
            session.commit()
        job_execution = query_job_execution.one()
        job_execution.cmdln = self.cmdln
        job_execution.cmdln = self.returncode
        job_execution.outputjson = self.outputjson
        job_execution.created = self.created
        job_execution.expires = self.expires
        job_execution.expired = self.expired


        session.add(job_execution)
        session.commit()
        return True



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



        query_job_def = session.query(model.job_def).\
                filter(model.job_def.uuid == uuid_def)
        if query_job_def.count() == 0:
            self.log.error("failed to find uuid_def:%s" % (uuid_def))
            return False


        query_job_namespace = session.query(model.job_namespace).\
                filter(model.job_def.uuid == uuid_def).\
                filter(model.job_namespace.id == model.job_def.fk_type)
        if query_job_namespace.count() == 0:
            self.log.error("failed to find job_namespace:%s" % (uuid_execution))
            return False

        job_namespace = query_job_namespace.one()
        job_def = query_job_def.one()
        self.cmdln_template = job_def.cmdln_template
        self.cmdln_paramters= job_def.cmdln_paramters


        set_subscribers = set()
        query_subscribers = session.query(model.job_def).\
                filter(model.job_def.uuid == uuid_def).\
                filter(model.job_triggers.source == model.job_def.id)
        for item in query_subscribers:
            set_subscribers.add(item.uuid)
        self.subscribers_list = set_subscribers
        self.log.info("subscribers=%s" % set_subscribers)

        set_publishers = set()
        query_publishers = session.query(model.job_def).\
                filter(model.job_def.uuid == uuid_def).\
                filter(model.job_triggers.dest == model.job_def.id)
        for item in query_publishers:
            set_publishers.add(item.uuid)
        self.publishers_list = set_publishers
        self.log.info("publishers=%s" % set_publishers)

        if uuid_execution == None:
            self.log.debug("No uuid_execution set")
            return True

        query_job_execution = session.query(model.job_execution).\
                filter(model.job_execution.uuid == uuid_execution)
        if query_job_execution.count() == 0:
            self.log.error("failed to find uuid_def:%s" % (uuid_execution))
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


        job_execution = query_job_execution.one()

        self.cmdln = job_execution.cmdln
        self.returncode = job_execution.cmdln
        self.outputjson = job_execution.outputjson
        self.created = job_execution.created
        self.expires = job_execution.expires
        self.expired = job_execution.expired



        return True

