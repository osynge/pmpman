import pmpmanager.db_devices as model
import logging

from base_calls import job_runner as bass_job_runner
import json
import datetime
import uuid
def Property(func):
    return property(**func())


class job_runner(bass_job_runner):
    def __init__(self):
        self.remotePrefix = None
        self.log = logging.getLogger("job_runner.lsblk_read")
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

        #self.log.debug("self.job_class=%s" % self.job_class)
        self.triggers = json.dumps([],sort_keys=True, indent=4)
        self.trig_parameters = json.dumps([],sort_keys=True, indent=4)

        session = kwargs.get('session', None)
        if session == None:
            self.log.warning("job_def_Add missing name")
            return
        #self.log.warning("running")
        instance_query = session.query(model.job_namespace,model.job_def,model.job_execution).\
            filter(model.job_execution.fk_update == model.job_def.id).\
            filter(model.job_def.fk_type == model.job_namespace.id).\
            order_by(model.job_execution.created)
        #self.log.warning("count=%s" % instance_query.count())
        #for item in instance_query:
        #    print item[0].name

        instance_query = session.query(model.job_namespace,model.job_def,model.job_execution).\
            filter(model.job_execution.fk_update == model.job_def.id).\
            filter(model.job_def.fk_type == model.job_namespace.id).\
            order_by(model.job_execution.created)
        self.log.warning("count=%s" % instance_query.count())
        for instance in instance_query:
            job_namespace = instance[0]
            job_def = instance[1]
            job_execution = instance[2]
            #self.log.error("job_namespace.name=%s" % job_namespace.name)
            #self.log.warning("sss=%s" % (job_execution.outputjson))
            if job_execution.outputjson == None:
                self.log.warning("sss=%s" % (job_execution.outputjson))
                continue
            read_output = json.loads(job_execution.outputjson)
            if read_output == None:
                self.log.error("Failed to laod JSON")
                continue
            for item in read_output:
                print item
                dest_query = session.query(model.job_namespace,model.job_def).\
                    filter(model.job_def.fk_type == model.job_namespace.id).\
                    filter(model.job_namespace.name == "udev_query")
                key = "/deev/sda"
                new_cmdln = "udevadm info -q all -n %s" % (key)
                self.log.debug("cmd=%s" % new_cmdln)
                for item in dest_query:
                    job_namespace = item[0]
                    job_def = item[1]
                    newjob_execution = model.job_execution()
                    newjob_execution.fk_update = job_def.id
                    newjob_execution.name = "udev_query"
                    newjob_execution.created = datetime.datetime.now()
                    newjob_execution.expires = datetime.datetime.now()
                    newjob_execution.outputjson = None
                    newjob_execution.returncode = None
                    newjob_execution.uuid = str(uuid.uuid1())
                    newjob_execution.triggers = "[]"
                    newjob_execution.cmdln = new_cmdln
                    session.add(newjob_execution)
                    session.commit()
            #session.delete(job_execution)
            session.commit()

        instance_query = session.query(model.job_namespace,model.job_def,model.job_execution).\
            filter(model.job_execution.fk_update == model.job_def.id).\
            filter(model.job_def.fk_type == model.job_namespace.id).\
            filter(model.job_namespace.name == "lsblk_read").\
            order_by(model.job_execution.created)
        for instance in instance_query:
            print instance

