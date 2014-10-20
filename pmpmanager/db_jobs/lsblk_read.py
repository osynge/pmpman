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
            self.log.warning("Update_Add missing name")
            return
        #self.log.warning("running")
        instance_query = session.query(model.job_namespace,model.Update,model.job_execution).\
            filter(model.job_execution.fk_update == model.Update.id).\
            filter(model.Update.fk_type == model.job_namespace.id).\
            order_by(model.job_execution.created)
        #self.log.warning("count=%s" % instance_query.count())
        #for item in instance_query:
        #    print item[0].name

        instance_query = session.query(model.job_namespace,model.Update,model.job_execution).\
            filter(model.job_execution.fk_update == model.Update.id).\
            filter(model.Update.fk_type == model.job_namespace.id).\
            filter(model.job_namespace.name == "lsblk_query").\
            order_by(model.job_execution.created)
        #self.log.warning("count=%s" % instance_query.count())
        for instance in instance_query:
            job_namespace = instance[0]
            Update = instance[1]
            job_execution = instance[2]
            #self.log.error("job_namespace.name=%s" % UpdateType.name)
            #self.log.warning("sss=%s" % (job_execution.outputjson))
            if job_execution.outputjson == None:
                continue
            read_output = json.loads(job_execution.outputjson)
            if read_output == None:
                continue
            for item in read_output:
                print item
                dest_query = session.query(model.job_namespace,model.Update).\
                    filter(model.Update.fk_type == model.job_namespace.id).\
                    filter(model.job_namespace.name == "udev_query")
                new_cmdln = "udevadm info -q all -n /dev/%s" % (key)

                for item in dest_query:
                    job_namespace = item[0]
                    Update = item[1]
                    newjob_execution = model.UpdateInstance()
                    newjob_execution.fk_update = Update.id
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

        instance_query = session.query(model.job_namespace,model.Update,model.job_execution).\
            filter(model.job_execution.fk_update == model.Update.id).\
            filter(model.Update.fk_type == model.job_namespace.id).\
            filter(model.job_namespace.name == "lsblk_read").\
            order_by(model.job_execution.created)
        for instance in instance_query:
            print instance

