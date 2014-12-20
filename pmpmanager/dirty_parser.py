
import job_exec

import logging
import json

from uuid import uuid4 as uuidgen
import db_devices as model


lsblk_wantedFields_suse = ["NAME","KNAME","MOUNTPOINT","PARTUUID","SERIAL","FSTYPE","RM","SIZE","FSTYPE","UUID","OWNER","GROUP","MODE","WWN","VENDOR","MAJ:MIN"]
lsblk_wantedFields = ["NAME", "KNAME", "MOUNTPOINT", "FSTYPE", "RM", "SIZE", "FSTYPE", "UUID", "OWNER", "GROUP", "MODE","MAJ:MIN"]

def init_blockdevice_scan(session):
    log = logging.getLogger("init_blockdevice_scan")
    BlockUpdateLsblk_count = session.query(model.BlockUpdateLsblk).count()
    if BlockUpdateLsblk_count > 0:
        return
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

    job_mount_query = job_exec.job_exec()
    job_mount_query.session = session
    job_mount_query.job_class = "mount_query"
    job_mount_query.save(
        session=session,
        uuid_tempate=new_uuid1,
        uuid_execution=new_uuid2,
        cmdln_template=new_uuid3,
        cmdln_paramters="",
        uuid_job_def="",
        )
    job_mount_query.inputjson = job_query_udev.outputjson
    job_mount_query.run()

    job_mount_read = job_exec.job_exec()
    job_mount_read.session = session
    job_mount_read.job_class = "mount_read"
    job_mount_read.save(
        session=session,
        uuid_tempate=new_uuid1,
        uuid_execution=new_uuid2,
        cmdln_template=new_uuid3,
        cmdln_paramters="",
        uuid_job_def="",
        )

    job_mount_read.inputjson = job_mount_query.outputjson
    job_mount_read.run()


def init_blockscan_postfix_lsblk(session):
    BlockUpdateLsblk = session.query(model.BlockUpdateLsblk).\
        order_by(model.BlockUpdateLsblk.created.desc())
    Latest = None
    Changed = False
    BlockUpdateLsblk_counter = 0
    for item in BlockUpdateLsblk:
        if BlockUpdateLsblk_counter == 0:
            Latest = item
        if BlockUpdateLsblk_counter < 22:
            continue
        session,delete(item)
        Changed = True
    if Changed:
        session.commit()
    if Latest == None:
        return

def init_blockscan_postfix_udev(session):
    BlockUpdateLsblk = session.query(model.BlockUpdateUdev).\
        order_by(model.BlockUpdateUdev.created.desc())
    Latest = None
    Changed = False
    BlockUpdateLsblk_counter = 0
    for item in BlockUpdateLsblk:
        if BlockUpdateLsblk_counter == 0:
            Latest = item
        if BlockUpdateLsblk_counter < 22:
            continue
        session,delete(item)
        Changed = True
    if Changed:
        session.commit()
    if Latest == None:
        return

def dirty_parser(session):
    log = logging.getLogger("dirty_parser")
    init_blockdevice_scan(session)
    init_blockscan_postfix_lsblk(session)


