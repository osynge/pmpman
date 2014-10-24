import pmpmanager.db_devices as model
import logging

from base_calls import job_exec as bass_job_exec
import json
import datetime
import uuid


def Property(func):
    return property(**func())


class job_exec(bass_job_exec):
    def __init__(self):
        self.remotePrefix = None
        self.log = logging.getLogger("job_exec.lsblk_read")
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


    def process_device(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("No session set")
            return False
        device = kwargs.get('device', None)
        if device == None:
            device = self.device
        if device == None:
            self.log.error("No device set")
            return False
        device = kwargs.get('device', None)
        if device == None:
            device = self.device
        details = kwargs.get('details', None)
        if details == None:
            self.log.error("No details set")
            return False
        #for key in details.keys():
        #    print key,details[key]

        found_FSTYPE  = details.get("FSTYPE")
        found_GROUP  = details.get("GROUP")
        found_KNAME  = details.get("KNAME")
        found_MAJ_MIN  = details.get("MAJ:MIN")
        found_MODE  = details.get("MODE")
        found_MOUNTPOINT  = details.get("MOUNTPOINT")
        found_NAME  = details.get("NAME")
        found_OWNER  = details.get("OWNER")
        found_PARTUUID  = details.get("PARTUUID")
        found_RM  = details.get("RM")
        found_SERIAL  = details.get("SERIAL")
        found_SIZE  = details.get("SIZE")
        found_UUID  = details.get("UUID")
        found_VENDOR  = details.get("VENDOR")
        found_WWN  = details.get("WWN")

        found_MAJ = None
        found_MIN = None
        if found_MAJ_MIN != None:
            found_MAJ,found_MIN = found_MAJ_MIN.split(":")

        self.log.info("found_NAME=%s" % (found_NAME))
        self.log.info("found_KNAME=%s" % (found_KNAME))

        devPath = "/dev/%s" % found_KNAME

        instance_query = session.query(model.Block).\
            filter(model.Block.devPath == devPath)
        if instance_query.count() == 0:
            self.log.info("Adding device:%s" % (found_KNAME))
            newblock = model.Block()
            newblock.devPath = devPath
            session.add(newblock)
            session.commit()
            instance_query = session.query(model.Block).\
                filter(model.Block.devPath == devPath)
        blockinDb = instance_query.one()
        changed = False
        if found_KNAME != None:
            if blockinDb.devPath != devPath:
                blockinDb.devPath = devPath
                changed = True
                self.log.info("Updating device '%s' devName with:%s" % (device,found_KNAME))
        if found_MAJ != None:
            if blockinDb.devicenodes_major != found_MAJ:
                blockinDb.devicenodes_major = found_MAJ
                changed = True
                self.log.info("Updating device '%s' devicenodes_major with:%s" % (device,found_MAJ))

        if found_MIN != None:
            if blockinDb.devicenodes_minor != found_MIN:
                blockinDb.devicenodes_minor = found_MIN
                changed = True
                self.log.info("Updating device '%s' devicenodes_minor with:%s" % (device,found_MIN))
        
        if found_RM != None:
            if blockinDb.device_removable != found_RM:
                blockinDb.device_removable = found_RM
                changed = True
                self.log.info("Updating device '%s' devicenodes_minor with:%s" % (device,found_RM))
        
        
        if changed:
            session.add(blockinDb)
            session.commit()



        information = model.BlockUpdateLsblk()
        information.fk_block = blockinDb.id

        information.created = datetime.datetime.now()
        information.lsblk_fstype = found_FSTYPE
        information.lsblk_group = found_GROUP
        information.lsblk_mode = found_MODE
        information.lsblk_mountpoint = found_MOUNTPOINT
        information.lsblk_name = found_NAME
        information.lsblk_owner = found_OWNER
        information.lsblk_partuuid = found_PARTUUID
        information.lsblk_rm = found_RM
        information.lsblk_serial = found_SERIAL
        information.lsblk_size = found_SIZE
        information.lsblk_uuid = found_UUID
        information.lsblk_vendor = found_VENDOR
        information.lsblk_wwn = found_WWN
        session.add(information)
        session.commit()


    def run(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("No session set")
            return False

        json_input = json.loads(self.inputjson)
        for item in json_input.keys():
            self.process_device(
                session=session,
                device = item,
                details = json_input[item]
                )


        output = []
        for device in json_input.keys():
            cmdln = "udevadm info -q all -n /dev/%s" % (device)
            device_output = {
                "cmdln" : cmdln
            }
            output.append(device_output)
        self.outputjson = json.dumps(output,sort_keys=True, indent=4)
        self.returncode = 0
        self.stdout = ""


