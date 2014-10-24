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
        self.log = logging.getLogger("job_exec.mount_read")
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("No session set")
            return False

        json_input = json.loads(self.inputjson)

        block_mounts_unfiltered_found = set()


        mounts_known = set()
        for item in json_input.keys():
            #self.log.error("json_input[%s]=%s" % (item,json_input[item]))
            block_mounts_unfiltered_found.add(item)
        blocks_known = set()
        block_query = session.query(model.Block)
        for item in block_query:
            blocks_known.add(item.devPath)

        #self.log.debug("blocks_known=%s" % blocks_known)

        block_mounts_filtered_found = blocks_known.intersection(block_mounts_unfiltered_found)
        self.log.error("block_mounts_filtered_found=%s" % block_mounts_filtered_found)


        filesystem_type_found = set()
        mountpoints_found = set()
        block_mountpoint_pair = set()
        for item in block_mounts_filtered_found:
            #self.log.error("process=%s" % item)
            mountpoint = json_input[item]["mountpoint"]
            mountpoints_found.add(mountpoint)
            filesystem_type = json_input[item]["filesystem"]
            filesystem_type_found.add(filesystem_type)
            block_mountpoint_pair.add((item,mountpoint))

        self.log.error("filesystem_type_found=%s" % filesystem_type_found)

        self.log.error("mountpoints_found=%s" % mountpoints_found)

        self.log.error("block_mounts_filtered_found=%s" % block_mounts_filtered_found)

        self.log.error("block_mountpoint_pair=%s" % block_mountpoint_pair)



        mountpoint_queried = set()
        mountpoint_query = session.query(model.MountPoint)
        for item in mountpoint_query:
            mountpoint_queried.add(item.MountPoint)

        mountpoint_extra = mountpoint_queried.difference(mountpoints_found)
        mountpoint_missing = mountpoints_found.difference(mountpoint_queried)

        self.log.error("mountpoint_extra=%s" % mountpoint_extra)
        self.log.error("mountpoint_missing=%s" % mountpoint_missing)

        # update mountpints
        changed = False
        for item in mountpoint_extra:
            foundMp = session.query(model.MountPoint).\
                filter(model.MountPoint.mountpoint == item)
            for mp in foundMp:
                session.delete(mp)
                changed = True
        for item in mountpoint_missing:
            newMp = model.MountPoint()
            newMp.mountpoint = item
            session.add(newMp)
            changed = True
        if changed:
            session.commit()


        # Delete extra mounts:
        Changed = False
        mount_query = session.query(model.Block,model.MountPoint,model.Mount).\
                filter(model.MountPoint.id == model.Mount.fk_mountpoint).\
                filter(model.Mount.fk_block == model.Block.id)
        for item in mount_query:
            block = item[0]
            mpount = item[1]
            mount = item[2]
            if block.devPath in block_mounts_filtered_found:
                if mpount.mountpoint in mountpoints_found:
                    continue
            session.delete(mount)
            Changed = True
        if Changed:
            session.commit()

        for item in block_mountpoint_pair:
            str_device = item[0]
            str_mountPoint = item[1]
            self.log.error("adding=%s,%s" % (item))
            device_query = session.query(model.Block).\
                filter(model.Block.devPath == str_device)
            device = device_query.one()
            mountPoint_query = session.query(model.MountPoint).\
                filter(model.MountPoint.mountpoint == str_mountPoint)
            mountPoint = mountPoint_query.one()
            newMount = model.Mount()
            newMount.fk_block = device.id
            newMount.fk_mountpoint = mountPoint.id
            session.add(newMount)
            session.commit()


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


