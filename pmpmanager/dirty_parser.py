
import job_exec 

import logging
import json

from uuid import uuid4 as uuidgen

lsblk_wantedFields = ["NAME","KNAME","MOUNTPOINT","PARTUUID","SERIAL","FSTYPE","RM","SIZE","FSTYPE","UUID","OWNER","GROUP","MODE","WWN","VENDOR","MAJ:MIN"]

def dirty_parser(session):
    log = logging.getLogger("dirty_parser")
    writer = job_exec.job_exec()
    writer.session = session
    new_uuid1 = str(uuidgen())
    new_uuid2 = str(uuidgen())
    new_uuid3 = str(uuidgen())
    writer.job_class = "lsblk_query"
    writer.cmdln = "lsblk  --output %s  --pairs" % ( ",".join(lsblk_wantedFields) )
    writer.save(
        session=session,
        uuid_tempate=new_uuid1,
        uuid_execution=new_uuid2,
        cmdln_template=new_uuid3,
        cmdln_paramters="",
        uuid_job_def="",
        )
    writer.run()
    
    reader = job_exec.job_exec()
    
    reader.session = session
    reader.job_class = "lsblk_read"
    reader.cmdln = ""
    reader.save(
        session=session,
        uuid_tempate=new_uuid1,
        uuid_execution=new_uuid2,
        cmdln_template=new_uuid3,
        cmdln_paramters=writer.outputjson,
        uuid_job_def="",
        )
    
    reader.inputjson = writer.outputjson
    reader.run()
    if reader.outputjson == None:
        return
    
    
    json_copntent = json.loads(reader.outputjson)
    for item in json_copntent:
        
        job_query_udev = job_exec.job_exec()
        job_query_udev.session = session
        job_query_udev.job_class = "udev_query"
        job_query_udev.cmdln = item["cmdln"]
        job_query_udev.save(
            session=session,
            uuid_tempate=new_uuid1,
            uuid_execution=new_uuid2,
            cmdln_template=new_uuid3,
            cmdln_paramters=writer.outputjson,
            uuid_job_def="",
            )
        job_query_udev.run()

        job_read_udev = job_exec.job_exec()
        job_read_udev.session = session
        job_read_udev.job_class = "udev_read"
        job_read_udev.save(
            session=session,
            uuid_tempate=new_uuid1,
            uuid_execution=new_uuid2,
            cmdln_template=new_uuid3,
            cmdln_paramters="",
            uuid_job_def="",
            )
        job_read_udev.inputjson = job_query_udev.outputjson
        job_read_udev.run()
