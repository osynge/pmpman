
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
        keys_required = set([
            "DEVLINKS",
            "DEVNAME",
            "DEVPATH",
            "DEVTYPE",
            "MAJOR",
            "MINOR",
            "SUBSYSTEM",
            "UDISKS_PRESENTATION_NOPOLICY",
            "USEC_INITIALIZED",
            ])
        keys_optional = set([
            "ID_BUS",
            "ID_FS_LABEL",
            "ID_FS_LABEL_ENC",
            "ID_FS_TYPE",
            "ID_FS_USAGE",
            "ID_FS_UUID",
            "ID_FS_UUID_ENC",
            "ID_FS_VERSION",
            "ID_INSTANCE",
            "ID_MODEL",
            "ID_MODEL_ENC",
            "ID_MODEL_ID",
            "ID_PART_ENTRY_NUMBER",
            "ID_PART_ENTRY_SCHEME",
            "ID_PART_ENTRY_SIZE",
            "ID_PART_ENTRY_TYPE",
            "ID_PART_TABLE_TYPE",
            "ID_PATH",
            "ID_PATH_TAG",
            "ID_REVISION",
            "ID_SERIAL",
            "ID_SERIAL_SHORT",
            "ID_TYPE",
            "ID_USB_DRIVER",
            "ID_USB_INTERFACE_NUM",
            "ID_USB_INTERFACES",
            "ID_VENDOR",
            "ID_VENDOR_ENC",
            "ID_VENDOR_ID",
            "TAGS",
            "UDISKS_PARTITION_SCHEME",
            "UDISKS_PARTITION_SIZE",
            ])
        known_keys = keys_optional.union(keys_required)
        input_dict = json.loads(inputjson)
        device = input_dict.get("DEVNAME")


        self.log.error("ID_FS_UUID=%s" % (input_dict.get("ID_FS_UUID")))
        self.log.error("ID_FS_LABEL=%s" % (input_dict.get("ID_FS_LABEL")))
        self.log.error("ID_FS_UUID=%s" % (input_dict.get("ID_FS_UUID_ENC")))
        self.log.error("ID_FS_LABEL=%s" % (input_dict.get("ID_FS_LABEL_ENC")))


        if input_dict.get("DEVNAME") == None:
            self.log.error("Missing:%s" % (device))
            return False
        foundkeys = set(input_dict.keys())
        extra = foundkeys.difference(known_keys)
        missing = keys_required.difference(foundkeys)
        for item in missing:
            self.log.info("Missing:%s" % (item))
        for item in extra:
            self.log.info("Unknown field when process:%s" % (item))
        if len(missing) > 0:
            self.log.error("Missing expected keys")
            return False

        # Update the database
        instance_query = session.query(model.Block).\
            filter(model.Block.devPath == input_dict.get("DEVNAME"))
        if instance_query.count() == 0:
            self.log.info("Adding device:%s" % (device))
            newblock = model.Block()
            newblock.devPath = device
            session.add(newblock)
            session.commit()
            instance_query = session.query(model.Block).\
                filter(model.Block.devPath == device)

        #populateDB

        blockinDb = instance_query.one()
        changed = False

        # Do required items.

        if input_dict.get("MAJOR") != None:
            if blockinDb.devicenodes_major != input_dict.get("MAJOR"):
                blockinDb.devicenodes_major = input_dict.get("MAJOR")
                changed = True
                self.log.info("Updating device '%s' devicenodes_major with:%s" % (device,input_dict.get("MAJOR")))
        if input_dict.get("MINOR") != None:
            if blockinDb.devicenodes_minor != input_dict.get("MINOR"):
                blockinDb.devicenodes_minor = input_dict.get("MINOR")
                changed = True
                self.log.info("Updating device '%s' devicenodes_minor with:%s" % (device,input_dict.get("MINOR")))
        if changed:
            session.add(blockinDb)
            session.commit()

        # Do optional items.
        if input_dict.get("ID_FS_TYPE") != None:
            FileSystemType_query = session.query(model.FileSystemType).\
                filter(model.FileSystemType.name_FileSystemType == input_dict.get("ID_FS_TYPE"))
            if FileSystemType_query.count() == 0:
                new_type = model.FileSystemType()
                new_type.name_FileSystemType = input_dict.get("ID_FS_TYPE")
                session.add(new_type)
                session.commit()
        if input_dict.get("ID_FS_UUID") != None:
            FileSystem_query = session.query(model.FileSystem).\
                filter(model.FileSystemType.name_FileSystemType == input_dict.get("ID_FS_TYPE")).\
                filter(model.FileSystemType.id == model.FileSystem.fk_fs_type).\
                filter(model.FileSystem.fs_uuid == input_dict.get("ID_FS_UUID"))

            if (FileSystem_query.count() == 0):
                FileSystemType_query = session.query(model.FileSystemType).\
                    filter(model.FileSystemType.name_FileSystemType == input_dict.get("ID_FS_TYPE"))
                FileSystemType = FileSystemType_query.one()
                new_type = model.FileSystem()
                new_type.fk_fs_type = FileSystemType.id
                new_type.fs_uuid = input_dict.get("ID_FS_UUID")
                new_type.fs_uuid_enc = input_dict.get("ID_FS_UUID_ENC")
                new_type.fs_label = input_dict.get("ID_FS_LABEL")
                new_type.fs_label_enc = input_dict.get("ID_FS_LABEL_ENC")
                session.add(new_type)
                session.commit()
                FileSystem_query = session.query(model.FileSystem).\
                    filter(model.FileSystemType.name_FileSystemType == input_dict.get("ID_FS_TYPE")).\
                    filter(model.FileSystemType.id == model.FileSystem.fk_fs_type).\
                    filter(model.FileSystem.fs_uuid == input_dict.get("ID_FS_UUID"))
            FileSystem = FileSystem_query.one()




        showlist = foundkeys.intersection(keys_optional)

        #for item in showlist:
        #    self.log.debug("input_dict:%s=%s" % (item, input_dict[item]))

