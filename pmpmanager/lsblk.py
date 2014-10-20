import subprocess
import time
import json
import re
import logging
import db_devices as model

import udev_query
import datetime
import uuid

def runpreloadcommand(cmd,timeout):
    process = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processRc = None
    handleprocess = True
    counter = 0
    stdout = ''
    stderr = ''
    while handleprocess:
        counter += 1
        time.sleep(1)
        cout,cerr = process.communicate()
        stdout += cout
        stderr += cerr
        process.poll()
        processRc = process.returncode
        if processRc != None:
            break
        if counter == timeout:
            os.kill(process.pid, signal.SIGQUIT)
        if counter > timeout:
            os.kill(process.pid, signal.SIGKILL)
            processRc = -9
            break
    return (processRc,stdout,stderr)


def lsblk():
    log = logging.getLogger("lsblk")
    
    wantedFields = ["NAME","KNAME","MOUNTPOINT","PARTUUID","SERIAL","FSTYPE","RM","SIZE","FSTYPE","UUID","OWNER","GROUP","MODE","WWN","VENDOR","MAJ:MIN"]
    lkfields = ",".join(wantedFields)
    command = "lsblk  --output %s  --pairs" % (lkfields)
    #log.debug("command=%s" % (command))
    processRc,stdout,stderr = runpreloadcommand(command,10)
    #log.debug("stdout=%s" % (stdout))
    output = {}
    for line in stdout.split("\n"):
        parsedKetValue = {}
        for key_value in re.split(r'[ ](?=[A-Z]+\b)', line):
            key_value_list = re.split(r'=', key_value)
            if len(key_value_list) != 2:
                continue
            parsedKetValue[str(key_value_list[0])] = str(key_value_list[1]).strip('"')
        
        if not 'KNAME' in parsedKetValue.keys():
            continue
        output[parsedKetValue['KNAME']] = parsedKetValue
   
    #json_line = str(output)
    #print json_line
    #parsedJson = json.loads(json_line)
    
    #print json.dumps(output,sort_keys=True, indent=4)
    return output



def updatdatabase(session=None):
    did_something = False
    log = logging.getLogger("updatdatabase")

    blocks_known = set()
    query_block = session.query(model.Block)
    if query_block.count() == 0:
        log.warning('No Blocks found')
    for block in query_block:
        if block.devName == None:
            continue
        blocks_known.add(block.devName)
    blockdevices = lsblk()
    blockfound = set(blockdevices.keys())
    
    blocks_discoverd = blockfound.difference(blocks_known)
    blocks_lost = blocks_known.difference(blockfound)
    id_update_type = None
    id_update = None
    if len(blocks_discoverd) > 0:
        find_existing = session.query(model.job_namespace,
                ).\
            filter(model.job_namespace.name == "kname_new")
        if find_existing.count() == 0:
            newjob_namespace = model.job_namespace()
            newjob_namespace.name = "kname_new"
            session.add(newjob_namespace)
            session.commit()
            find_existing = session.query(model.job_namespace,).\
                filter(model.job_namespace.name == "kname_new")
            id_update_type = int(find_existing.first().id)
        else:
            id_update_type = int(find_existing.first().id)
            
        find_existing = session.query(model.Update).\
            filter(model.Update.fk_type == id_update_type)
        if find_existing.count() == 0:
            newUpdate = model.Update()
            newUpdate.fk_type = id_update_type
            newUpdate.cmdln_template = "updatdatabase"
            newUpdate.cmdln_paramters = "updatdatabase"
            session.add(newUpdate)
            session.commit()
            find_existing = session.query(model.Update).\
                filter(model.Update.fk_type == id_update_type)
        id_update = int(find_existing.first().id)
        find_existing = session.query(model.job_execution).\
            filter(model.job_execution.fk_update == id_update)

        if find_existing.count() == 0:
            newUpdate = model.job_execution()
            newUpdate.fk_update = id_update
            newUpdate.cmdln = "here is is"
            newUpdate.created = datetime.datetime.now()
            newUpdate.uuid = str(uuid.uuid1())
            session.add(newUpdate)
            session.commit()
            
    for device_key in blocks_discoverd:
        find_existing = session.query(model.job_execution).\
            filter(model.Block.devName == device_key).\
            filter(model.Update.fk_type == model.job_namespace.id).\
            filter("lsblk" == model.job_namespace.name).\
            filter(model.job_execution.fk_update == model.job_namespace.id)
        for i in find_existing:
            log.debug("i=%s"  % (i))            
        #log.debug("device_details=%s"  % (device_details))
        device_details = blockdevices[device_key]
        devName = device_details.get("KNAME")
        if devName == None:
            continue
        newImage = model.Block()
        newImage.devName = devName
        #log.debug("newImage.devName=%s"  % (newImage.devName))
        newImage.idVendor = device_details.get("ID_VENDOR")
        newImage.idProduct = device_details.get("DEVNAME")
        newImage.devicenodes_major = device_details.get("MAJOR")
        newImage.devicenodes_minor = device_details.get("MINOR")
        newImage.device_removable = device_details.get("RM")
        newImage.mountpoint = device_details.get('MOUNTPOINT')
        newImage.fk_update = id_update
        session.add(newImage)
        session.commit()
        did_something = True
    if did_something:
        find_existing = session.query(model.job_namespace,
                ).\
            filter(model.job_namespace.name == "kname_new")
        if find_existing.count() == 0:
            newjob_namespace = model.job_namespace()
            newjob_namespace.name = "kname_new"
            session.add(newjob_namespace)
        find_existing = session.query(model.Update,
                ).\
            filter(model.Update.fk_type ==model.job_namespace.id).\
            filter(model.job_namespace.name == "kname_new")
        if find_existing.count() == 0:        
            index = None
            find_type = session.query(model.job_namespace,
                    ).\
                filter(model.job_namespace.name == "kname_new")
            if find_type.count() == 0:
                newjob_namespace = model.job_namespace()
                newjob_namespace.name = "kname_new"
                session.add(newjob_namespace)
                session.commit()
            find_type = session.query(model.job_namespace,
                    ).\
                filter(model.job_namespace.name == "kname_new")
            typeID = int(find_type.one().id)
            newjob_namespace = model.Update()
            newjob_namespace.fk_type = typeID
            newjob_namespace.name = "kname_new"
            session.add(newjob_namespace)
            session.commit()
        find_existing = session.query(model.Update,
                ).\
            filter(model.Update.fk_type ==model.job_namespace.id).\
            filter(model.job_namespace.name == "kname_new")   
        
            
    for device_key in blocks_discoverd:
        find_existing = session.query(model.job_execution).\
            filter(model.Block.devName == device_key).\
            filter(model.Update.fk_type == model.job_namespace.id).\
            filter("lsblk" == model.job_namespace.name).\
            filter(model.job_execution.fk_update == model.job_namespace.id)
        
    for device_key in blocks_lost:
        log.warning('Code not complete')
    
    return blockdevices

