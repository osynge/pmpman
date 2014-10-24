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


import jobs.lsblk_query as job_runner_lsblk_query
import jobs.lsblk_read as job_runner_lsblk_read

import jobs.udev_query as job_runner_udev_query
import jobs.udev_read as job_runner_udev_read
import jobs.no_ops as job_runner_no_ops
import jobs.mount_query as job_runner_mount_query
import jobs.mount_read as job_runner_mount_read
import db_devices as model




from sqlalchemy.orm import aliased

class job_exec(object):
    """Facade class for mulitple implementations of a job junner,
    Should be robust for setting the impleemntation or attributes
    in any order."""

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger("job_exec")
        self.job_classes = {
            "no_ops" : job_runner_no_ops,
            "kname_new" :  job_runner_udev_read,
            "udev_query" : job_runner_udev_query ,
            "lsblk_query" : job_runner_lsblk_query,
            "lsblk" : job_runner_lsblk_query,
            "udev_read" : job_runner_udev_read,
            "lsblk_read" : job_runner_lsblk_read,
            "mount_query" : job_runner_mount_query,
            "mount_read" : job_runner_mount_read,
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



            tmpJobRnner = self.job_classes[name].job_exec()
            tmpJobRnner.job_class = name
            tmpJobRnner.session = self.session
            tmpJobRnner.cmdln = self.cmdln
            tmpJobRnner.returncode = self.returncode
            tmpJobRnner.outputjson = self.outputjson
            tmpJobRnner.inputjson = self.inputjson
            tmpJobRnner.created = self.created
            tmpJobRnner.expires = self.expires
            tmpJobRnner.expired = self.expired
            tmpJobRnner.uuid_execution = self.uuid_execution
            tmpJobRnner.state = self.state

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
    def inputjson():
        doc = "Remote upload prefix"
        def fget(self):
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if hasattr(self._job_runnerImp,'inputjson'):
                        return self._job_runnerImp.inputjson
                    else:
                        return None
            if hasattr(self, '_inputjson'):
                return self._inputjson

        def fset(self, value):
            self._inputjson = value
            if hasattr(self, '_job_runnerImp'):
                if self._job_runnerImp != None:
                    if self._job_runnerImp.inputjson != value:
                        self._job_runnerImp.inputjson = value
        def fdel(self):
            del self._inputjson
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

    def enqueue(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("enqueue:No session set")
            return False

        cmdln_paramters = kwargs.get('cmdln_paramters', None)
        if cmdln_paramters == None:
           cmdln_paramters = cmdln_paramters
        if cmdln_paramters == None:
            self.log.error("No cmdln_paramters set")
            raise InputError("No cmdln_paramters set")


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
        enqueue_job_runner.cmdln_paramters = cmdln_paramters

        # Now save queued request
        enqueue_job_runner.save(session = session,
            )

        session.commit()

        return True

    def run(self, *args, **kwargs):
        if hasattr(self, '_job_runnerImp'):
            return self._job_runnerImp.run(*args, **kwargs)


    def save(self, *args, **kwargs):
        #self.log.debug("save")
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            sdsdfsdfs
            self.log.error("No session set")
            raise InputError("No session set")

        job_class = kwargs.get('job_class', None)
        if job_class == None:
           job_class = self.job_class
        if job_class == None:
            self.log.error("No job_class set")
            raise InputError("No job_class set")

        uuid_tempate = kwargs.get('uuid_tempate', None)
        if uuid_tempate == None:
            uuid_tempate = self.uuid_tempate
        if uuid_tempate == None:
            self.log.error("No uuid_tempate set")
            raise InputError("No uuid_tempate set")

        cmdln_template = kwargs.get('cmdln_template', None)
        if cmdln_template == None:
            if hasattr(self, 'cmdln_template'):
                cmdln_template = self.cmdln_template
        if cmdln_template == None:
            self.log.error("No cmdln_template set")
            raise InputError("No cmdln_template set")

        cmdln_paramters = kwargs.get('cmdln_paramters', None)
        if cmdln_paramters == None:
           cmdln_paramters = cmdln_paramters
        if cmdln_paramters == None:
            self.log.error("No cmdln_paramters set")
            raise InputError("No cmdln_paramters set")


        # Now the ones we dont need
        uuid_execution = kwargs.get('uuid_execution', None)
        if uuid_execution == None:
           uuid_execution = self.uuid_execution
        if uuid_execution == None:
            self.log.error("No uuid_execution set")
            raise InputError("No uuid_execution set")


        uuid_job_def = kwargs.get('uuid_job_def', None)
        if uuid_job_def == None:
            if hasattr(self, 'uuid_job_def'):
                uuid_job_def = self.uuid_job_def
        if uuid_job_def == None:
            self.log.error("No uuid_job_def set")
            raise InputError("No uuid_job_def set")















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
                filter(model.job_def.uuid_job_def == uuid_execution)

        if query_job_def.count() == 0:
            job_def = model.job_def()
            job_def.fk_type = job_namespace.id
            job_def.cmdln_template = cmdln_template
            job_def.uuid_job_def = uuid_execution
            session.add(job_def)
            session.commit()
            query_job_def = session.query(model.job_def).\
                filter(model.job_def.uuid_job_def == uuid_execution)

        job_def = query_job_def.one()
        job_def.cmdln_template = cmdln_template
        job_def.cmdln_paramters = cmdln_paramters

        job_def.fk_type = job_namespace.id
        session.add(job_def)
        session.commit()



        subscribers_found = set()
        publishers_found = set()

        source_job = aliased(model.job_def, name='source_job')
        dest_job = aliased(model.job_def, name='dest_job')

        query_subscribers = session.query(dest_job.uuid_job_def).\
                filter(source_job.uuid_job_def == uuid_execution).\
                filter(model.job_triggers.dest == dest_job.id).\
                filter(model.job_triggers.source == source_job.id)

        for item in query_subscribers:
            subscribers_found.add(item.uuid)
        query_publishers = session.query(source_job.uuid_job_def).\
                filter(dest_job.uuid_job_def == uuid_execution).\
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

