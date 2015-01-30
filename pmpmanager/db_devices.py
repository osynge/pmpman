from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import mapper

from sqlalchemy import ForeignKey

from sqlalchemy.orm import backref
try:
    from sqlalchemy.orm import relationship
except:
    from sqlalchemy.orm import relation as relationship


from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

from sqlalchemy.schema import UniqueConstraint
import uuid

##########################################
# makes key value tables to increase flexibility.

Base = declarative_base()

class client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(40),nullable = False,unique=True)
    client_job_latest = Column(Integer,nullable = True)
    client_sock = Column(String(255),nullable = True ,unique=True)
    
    def __init__(self, *args, **kwargs):
        name = kwargs.get('name', None)
        pass


class client_job(Base):
    __tablename__ = 'client_job'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime,nullable = False)
    expires = Column(DateTime,nullable = False)
    fk_client = Column(Integer, ForeignKey(client.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    uuid = Column(String(40),nullable = False,unique=True)
    session_id = Column(String(40),unique=True, nullable = False)
    def __init__(self, *args, **kwargs):
        name = kwargs.get('name', None)
        if name != None:
           self.name = name



class job_namespace(Base):
    __tablename__ = 'job_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(1024),nullable = False,unique=True)

    def __init__(self, *args, **kwargs):
        name = kwargs.get('name', None)
        if name != None:
           self.name = name


class job_state(Base):
    __tablename__ = 'job_state'
    id = Column(Integer, primary_key=True)
    name = Column(String(24),nullable = False,unique=True)
    def __init__(self, *args, **kwargs):
        name = kwargs.get('name', None)
        if name != None:
           self.name = name




class job_def(Base):
    """Stores reoccuring jobs"""
    __tablename__ = 'job_def'
    id = Column(Integer, primary_key=True)
    fk_type = Column(Integer, ForeignKey(job_namespace.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    cmdln_template = Column(String(1024),unique=False,nullable = False)
    cmdln_paramters = Column(String(1024),unique=False)
    latest = Column(Integer,nullable = True)
    reocuring = Column(Integer,nullable = False)
    uuid_job_def = Column(String(40),unique=True, nullable = False)
    lifetime = Column(Integer,nullable = True)
    def __init__(self, *args, **kwargs):
        latest = kwargs.get('latest', None)
        if latest != None:
            self.latest = latest
        reocuring = kwargs.get('reocuring', None)
        if reocuring != None:
            self.reocuring = reocuring
        else:
            self.reocuring = 0

        cmdln_template = kwargs.get('cmdln_template', None)
        if cmdln_template != None:
            self.cmdln_template = cmdln_template
        cmdln_paramters = kwargs.get('cmdln_paramters', None)
        if cmdln_paramters != None:
            self.cmdln_paramters = cmdln_paramters



class job_execution(Base):
    """stores job runs.
    """
    __tablename__ = 'job_scheduling'
    id = Column(Integer, primary_key=True)
    fk_update = Column(Integer, ForeignKey(job_def.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    fk_state = Column(Integer, ForeignKey(job_def.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    cmdln = Column(String(1024),unique=False,nullable = True)
    uuid_job_execution = Column(String(40),unique=True,nullable = False)


    returncode = Column(Integer,nullable = True)
    outputjson = Column(String(1024))
    created = Column(DateTime,nullable = False)
    expires = Column(DateTime,nullable = True)
    expired = Column(DateTime,nullable = True)
    finshed = Column(DateTime,nullable = True)
    triggers = Column(String(1024),nullable = False)
    trig_parameters = Column(String(1024),nullable = False)
    def __init__(self, *args, **kwargs):
        returncode = kwargs.get('returncode', None)
        if returncode != None:
           self.returncode = returncode
        outputjson = kwargs.get('outputjson', None)
        if outputjson != None:
           self.outputjson = outputjson
        created = kwargs.get('created', None)
        if created != None:
           self.created = created
        expires = kwargs.get('expires', None)
        if expires != None:
            self.expires = expires
        finshed = kwargs.get('finshed', None)
        if finshed != None:
            self.finshed = finshed
        fk_update = kwargs.get('fk_update', None)
        if fk_update != None:
           self.fk_update = fk_update
        expired = kwargs.get('expired', None)
        if expired != None:
            self.expired = expired
        fk_update = kwargs.get('fk_update', None)
        cammand_line = kwargs.get('cammand_line', None)
        if cammand_line != None:
            self.cmdln = cammand_line
        cmdln_paramters = kwargs.get('cmdln_paramters', None)
        if cmdln_paramters != None:
            self.cmdln = cammand_line
        self.triggers = kwargs.get('triggers', None)
        self.trig_parameters = kwargs.get('trig_parameters', "[]")
        this_uuid_opt_01 = kwargs.get('uuid', None)
        this_uuid_opt_02 = kwargs.get('uuid_job_execution', None)

        # pick best default

        this_uuid = this_uuid_opt_01
        if this_uuid_opt_02 != None:
            this_uuid = this_uuid_opt_02


        if this_uuid == None:
            self.uuid = str(uuid.uuid4())
        else:
            self.uuid = str(this_uuid)


class job_triggers(Base):
    """stores job runs.
    """
    __tablename__ = 'JOB_TRIGGERS'
    id = Column(Integer, primary_key=True)
    sk_uuid = Column(String(30),unique=False,nullable = False)
    source = Column(Integer, ForeignKey(job_def.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    dest = Column(Integer, ForeignKey(job_def.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)

    def __init__(self, *args, **kwargs):
        sk_uuid = kwargs.get('sk_uuid', None)
        if sk_uuid != None:
           self.sk_uuid = sk_uuid
        source = kwargs.get('source', None)
        if source != None:
           self.source = source
        dest = kwargs.get('dest', None)
        if dest != None:
           self.dest = dest





class Block(Base):
    __tablename__ = 'Block'
    id = Column(Integer, primary_key=True)
    devPath = Column(String(255),nullable = False,unique=True)
    devicenodes_major = Column(String(10),nullable = True)
    devicenodes_minor = Column(String(10),nullable = True)
    device_removable = Column(Integer,nullable = True)

    def __init__(self, *args, **kwargs):

        idVendor = kwargs.get('idVendor', None)
        if idVendor != None:
           self.idVendor = uuid.uuid()

        idProduct = kwargs.get('idProduct', None)
        if idProduct != None:
           self.idProduct = idProduct
        devicenodes_major = kwargs.get('devicenodes_major', None)
        if devicenodes_major != None:
           self.devicenodes_major = devicenodes_major
        devicenodes_minor = kwargs.get('devicenodes_minor', None)
        if devicenodes_minor != None:
           self.devicenodes_minor = devicenodes_minor
        device_removable = kwargs.get('device_removable', None)
        if device_removable != None:
           self.device_removable = device_removable


    def __repr__(self):
        return "<Block('%s')>" % (self.devPath)




class BlockUpdateUdev(Base):
    __tablename__ = 'BlockUpdateUdev'
    id = Column(Integer, primary_key=True)
    fk_block = Column(Integer, ForeignKey(job_def.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)

    created = Column(DateTime,nullable = False)

    devicenodes_major = Column(String(10),nullable = True)
    devicenodes_minor = Column(String(10),nullable = True)
    device_removable = Column(Integer,nullable = True)


    udev_id_vendor = Column(String(100),unique=False)
    udev_id_vendor_id = Column(String(100),unique=False)
    udev_id_vendor_enc = Column(String(100),unique=False)
    udev_id_product = Column(String(100),nullable = True)
    udev_id_model = Column(String(100),nullable = True)
    udev_id_fs_label_enc = Column(String(100),nullable = True)
    udev_id_fs_label = Column(String(100),nullable = True)
    udev_id_fs_type = Column(String(100),nullable = True)
    udev_id_fs_usage = Column(String(100),nullable = True)
    udev_id_fs_uuid = Column(String(100),nullable = True)
    udev_id_fs_uuid_enc = Column(String(100),nullable = True)
    udev_id_version = Column(String(100),nullable = True)
    udev_id_fs_model = Column(String(100),nullable = True)
    udev_id_fs_model_enc = Column(String(100),nullable = True)
    udev_id_fs_model_id = Column(String(100),nullable = True)
    udev_id_serial = Column(String(100),nullable = True)
    udev_id_serial_short = Column(String(100),nullable = True)
    udev_id_type = Column(String(100),nullable = True)
    udev_id_udiscs_partiton_scheme = Column(String(10),nullable = True)
    udev_id_udiscs_partiton_size = Column(Integer,nullable = True)

    def __init__(self, *args, **kwargs):

        idVendor = kwargs.get('idVendor', None)
        if idVendor != None:
           self.idVendor = uuid.uuid()

        idProduct = kwargs.get('idProduct', None)
        if idProduct != None:
           self.idProduct = idProduct
        devicenodes_major = kwargs.get('devicenodes_major', None)
        if devicenodes_major != None:
           self.devicenodes_major = devicenodes_major
        devicenodes_minor = kwargs.get('devicenodes_minor', None)
        if devicenodes_minor != None:
           self.devicenodes_minor = devicenodes_minor
        device_removable = kwargs.get('device_removable', None)
        if device_removable != None:
           self.device_removable = device_removable


    def __repr__(self):
        return "<BlockUpdateUdev('%s')>" % (self.devPath)




class BlockUpdateLsblk(Base):
    __tablename__ = 'BlockUpdateLsblk'
    id = Column(Integer, primary_key=True)
    fk_block = Column(Integer, ForeignKey(job_def.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    created = Column(DateTime,nullable = False)

    devicenodes_major = Column(String(10),nullable = True)
    devicenodes_minor = Column(String(10),nullable = True)
    device_removable = Column(Integer,nullable = True)

    lsblk_fstype = Column(Integer,nullable = True)
    lsblk_group = Column(Integer,nullable = True)
    lsblk_mode = Column(Integer,nullable = True)
    lsblk_mountpoint = Column(Integer,nullable = True)
    lsblk_name = Column(Integer,nullable = True)
    lsblk_owner = Column(Integer,nullable = True)
    lsblk_partuuid = Column(Integer,nullable = True)
    lsblk_rm = Column(Integer,nullable = True)

    lsblk_serial = Column(Integer,nullable = True)
    lsblk_size = Column(Integer,nullable = True)
    lsblk_uuid = Column(Integer,nullable = True)
    lsblk_vendor = Column(Integer,nullable = True)
    lsblk_wwn = Column(Integer,nullable = True)
    def __init__(self, *args, **kwargs):

        idVendor = kwargs.get('idVendor', None)
        if idVendor != None:
           self.idVendor = uuid.uuid()

        idProduct = kwargs.get('idProduct', None)
        if idProduct != None:
           self.idProduct = idProduct
        devicenodes_major = kwargs.get('devicenodes_major', None)
        if devicenodes_major != None:
           self.devicenodes_major = devicenodes_major
        devicenodes_minor = kwargs.get('devicenodes_minor', None)
        if devicenodes_minor != None:
           self.devicenodes_minor = devicenodes_minor
        device_removable = kwargs.get('device_removable', None)
        if device_removable != None:
           self.device_removable = device_removable


    def __repr__(self):
        return "<BlockUpdateLsblk('%s','%s')>" % (self.fk_block, self.created)

class FileSystemType(Base):
    __tablename__ = 'FileSystemType'
    id = Column(Integer, primary_key=True)
    fk_block = Column(Integer, ForeignKey(Block.id, onupdate="CASCADE", ondelete="CASCADE"))
    name_FileSystemType = Column(String(64),nullable = True,unique=True)

    def __init__(self, *args, **kwargs):
        fk_block = kwargs.get('fk_block', None)
        if fk_block != None:
           self.fk_block = uuid.uuid()
        name_FileSystemType = kwargs.get('name_FileSystemType', None)
        if name_FileSystemType != None:
           self.name_FileSystemType = uuid.uuid()


    def __repr__(self):
        return "<FileSystemType('%s','%s', '%s')>" % (self.fkEndorser, self.key, self.value)



class FileSystem(Base):
    __tablename__ = 'FileSystem'
    id = Column(Integer, primary_key=True)
    fk_fs_type = Column(Integer, ForeignKey(FileSystemType.id, onupdate="CASCADE", ondelete="CASCADE"))
    fs_uuid = Column(String(40),unique=True,nullable = False)
    fs_label = Column(String(40),nullable = True)
    fs_uuid_enc = Column(String(40),unique=True,nullable = False)
    fs_label_enc = Column(String(40),nullable = True)

    # explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint('fkEndorser', 'key')
    def __init__(self, *args, **kwargs):
        fk_fs_type = kwargs.get('fk_fs_type', None)
        if fk_fs_type != None:
           self.fk_fs_type = uuid.uuid()
        fs_uuid = kwargs.get('fs_uuid', None)
        if fs_uuid != None:
           self.fs_uuid = uuid.uuid()

    def __repr__(self):
        return "<Filesystem('%s','%s', '%s')>" % (self.fkEndorser, self.key, self.value)



class MountPoint(Base):
    __tablename__ = 'MountPoint'
    id = Column(Integer, primary_key=True)
    mountpoint = Column(String(512),nullable = False,unique=True)
    def __init__(self, *args, **kwargs):
        mountpoint = kwargs.get('mountpoint', None)
        if mountpoint != None:
           self.mountpoint = mountpoint
    def __repr__(self):
        return "<MountPoint('%s')>" % (self.mountpoint)



class Mount(Base):
    __tablename__ = 'Mount'
    id = Column(Integer, primary_key=True)
    fk_block = Column(Integer, ForeignKey(Block.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    fk_mountpoint = Column(Integer, ForeignKey(Block.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    fk_filesystem = Column(Integer, ForeignKey(Block.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = True)
    def __init__(self, *args, **kwargs):
        fk_block = kwargs.get('fk_block', None)
        if fk_block != None:
           self.fk_block = fk_block
        fk_mountpoint = kwargs.get('fk_mountpoint', None)
        if fk_mountpoint != None:
           self.fk_mountpoint = fk_mountpoint
        fk_filesystem = kwargs.get('fk_filesystem', None)
        if fk_filesystem != None:
           self.fk_filesystem = fk_filesystem
    def __repr__(self):
        return "<Mount('%s','%s', '%s')>" % (self.fkEndorser, self.key, self.value)

class FileStore(Base):
    __tablename__ = 'FileStore'
    id = Column(Integer, primary_key=True)
    id_fs_type = Column(Integer, ForeignKey(FileSystemType.id, onupdate="CASCADE", ondelete="CASCADE"))
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return "<Filesystem('%s','%s', '%s')>" % (self.fkEndorser, self.key, self.value)






class ManagedFiles(Base):
    __tablename__ = 'ManagedFiles'
    id = Column(Integer, primary_key=True)
    fk_block = Column(Integer, ForeignKey(Block.id, onupdate="CASCADE", ondelete="CASCADE"))
    mountpoint = Column(String(512),nullable = True,unique=True)
    key = Column(String(200),nullable = False)
    value = Column(String(200),nullable = False)
    # explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint('fkEndorser', 'key')
    def __init__(self, *args, **kwargs):
        self.fkEndorser = imagelist
        self.key = key
        self.value = value
    def __repr__(self):
        return "<ManagedFiles('%s','%s', '%s')>" % (self.fkEndorser, self.key, self.value)




def init(engine):
    Base.metadata.create_all(engine)
