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
        instance_query = session.query(model.UpdateType,model.Update,model.UpdateInstance).\
            filter(model.UpdateInstance.fk_update == model.Update.id).\
            filter(model.Update.fk_type == model.UpdateType.id).\
            order_by(model.UpdateInstance.created)
        #self.log.warning("count=%s" % instance_query.count())
        #for item in instance_query:
        #    print item[0].name
        
        instance_query = session.query(model.UpdateType,model.Update,model.UpdateInstance).\
            filter(model.UpdateInstance.fk_update == model.Update.id).\
            filter(model.Update.fk_type == model.UpdateType.id).\
            filter(model.UpdateType.name == "lsblk_query").\
            order_by(model.UpdateInstance.created)
        #self.log.warning("count=%s" % instance_query.count())
        for instance in instance_query:
            UpdateType = instance[0]
            Update = instance[1]
            UpdateInstance = instance[2]
            #self.log.error("UpdateType.name=%s" % UpdateType.name)
            #self.log.warning("sss=%s" % (UpdateInstance.outputjson))
            if UpdateInstance.outputjson == None:
                continue
            read_output = json.loads(UpdateInstance.outputjson)
            if read_output == None:
                continue
            for item in read_output:
                print item
                dest_query = session.query(model.UpdateType,model.Update).\
                    filter(model.Update.fk_type == model.UpdateType.id).\
                    filter(model.UpdateType.name == "udev_query")
                new_cmdln = "udevadm info -q all -n /dev/%s" % (key)
                
                for item in dest_query:
                    UpdateType = item[0]
                    Update = item[1]
                    newUpdateInstance = model.UpdateInstance()
                    newUpdateInstance.fk_update = Update.id
                    newUpdateInstance.name = "udev_query"
                    newUpdateInstance.created = datetime.datetime.now()
                    newUpdateInstance.expires = datetime.datetime.now()
                    newUpdateInstance.outputjson = None
                    newUpdateInstance.returncode = None
                    newUpdateInstance.uuid = str(uuid.uuid1())
                    newUpdateInstance.triggers = "[]"               
                    newUpdateInstance.cmdln = new_cmdln        
                    session.add(newUpdateInstance)
                    session.commit()
            #session.delete(UpdateInstance)
            session.commit()
        
        instance_query = session.query(model.UpdateType,model.Update,model.UpdateInstance).\
            filter(model.UpdateInstance.fk_update == model.Update.id).\
            filter(model.Update.fk_type == model.UpdateType.id).\
            filter(model.UpdateType.name == "lsblk_read").\
            order_by(model.UpdateInstance.created)
        for instance in instance_query:
            print instance

