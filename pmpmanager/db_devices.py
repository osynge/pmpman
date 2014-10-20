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


class UpdateType(Base):
    __tablename__ = 'job_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(1024),nullable = False,unique=True)
    lifetime = Column(Integer,nullable = True)
    def __init__(self, *args, **kwargs):
        name = kwargs.get('name', None)
        if name != None:
           self.name = name
        self.lifetime = kwargs.get('lifetime', 60)

class Update(Base):
    """Stores reoccuring jobs"""
    __tablename__ = 'job_def'
    id = Column(Integer, primary_key=True)
    fk_type = Column(Integer, ForeignKey(UpdateType.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    cmdln_template = Column(String(1024),unique=False,nullable = False)
    cmdln_paramters = Column(String(1024),unique=False)
    latest = Column(Integer,nullable = True)
    reocuring = Column(Integer,nullable = False)
    uuid = Column(String(30),unique=False,nullable = False)
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
    fk_update = Column(Integer, ForeignKey(Update.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    
    cmdln = Column(String(1024),unique=False,nullable = True)
    uuid = Column(String(30),unique=False,nullable = False)
    
    
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
        this_uuid = kwargs.get('uuid', None)
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
    source = Column(Integer, ForeignKey(Update.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    dest = Column(Integer, ForeignKey(Update.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    
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
    fk_update = Column(Integer, ForeignKey(Update.id, onupdate="CASCADE", ondelete="CASCADE"),nullable = False)
    devName= Column(String(100),nullable = False,unique=True)
    
    idVendor = Column(String(100),unique=False)
    idProduct = Column(String(100),nullable = True)
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
        return "<USB_Bus_Hw('%s')>" % (self.subject)


class FilesystemType(Base):
    __tablename__ = 'FilesystemType'
    id = Column(Integer, primary_key=True)
    fk_block = Column(Integer, ForeignKey(Block.id, onupdate="CASCADE", ondelete="CASCADE"))
    fk_update = Column(Integer, ForeignKey(Update.id, onupdate="CASCADE", ondelete="CASCADE"))
    name = Column(String(64),nullable = True,unique=True)
    
    key = Column(String(200),nullable = False)
    value = Column(String(200),nullable = False)
    # explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint('fkEndorser', 'key')
    def __init__(self,imagelist,key,value):
        self.fkEndorser = imagelist
        self.key = key
        self.value = value
    def __repr__(self):
        return "<EndorserMetadata('%s','%s', '%s')>" % (self.fkEndorser, self.key, self.value)



class Filesystem(Base):
    __tablename__ = 'Filesystem'
    id = Column(Integer, primary_key=True)
    id_fs_type = Column(Integer, ForeignKey(FilesystemType.id, onupdate="CASCADE", ondelete="CASCADE"))
    mountpoint = Column(String(512),nullable = True,unique=True)
    key = Column(String(200),nullable = False)
    value = Column(String(200),nullable = False)
    # explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint('fkEndorser', 'key')
    def __init__(self,imagelist,key,value):
        self.fkEndorser = imagelist
        self.key = key
        self.value = value
    def __repr__(self):
        return "<EndorserMetadata('%s','%s', '%s')>" % (self.fkEndorser, self.key, self.value)



class Mount(Base):
    __tablename__ = 'Mount'
    id = Column(Integer, primary_key=True)
    fkEndorser = Column(Integer, ForeignKey(Block.id, onupdate="CASCADE", ondelete="CASCADE"))
    mountpoint = Column(String(512),nullable = True,unique=True)
    key = Column(String(200),nullable = False)
    value = Column(String(200),nullable = False)
    # explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint('fkEndorser', 'key')
    def __init__(self,imagelist,key,value):
        self.fkEndorser = imagelist
        self.key = key
        self.value = value
    def __repr__(self):
        return "<EndorserMetadata('%s','%s', '%s')>" % (self.fkEndorser, self.key, self.value)

def init(engine):
    Base.metadata.create_all(engine)
