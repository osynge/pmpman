import subprocess
import time

import logging

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

def udevadm_info(device):
    log = logging.getLogger("udevadm_info")
    eparmas_interesting = [
'DEVLINKS',
'DEVNAME',
'DEVPATH',
'DEVTYPE',
'ID_BUS',
'ID_FS_LABEL',
'ID_FS_LABEL_ENC',
'ID_FS_TYPE',
'ID_FS_USAGE',
'ID_FS_UUID',
'ID_FS_UUID_ENC',
'ID_FS_VERSION',
'ID_INSTANCE',
'ID_MODEL',
'ID_MODEL_ENC',
'ID_MODEL_ID',
'ID_PART_TABLE_TYPE',
'ID_PATH',
'ID_PATH_TAG',
'ID_REVISION',
'ID_SERIAL',
'ID_SERIAL_SHORT',
'ID_TYPE',
'ID_USB_DRIVER',
'ID_USB_INTERFACES',
'ID_USB_INTERFACE_NUM',
'ID_VENDOR',
'ID_VENDOR_ENC',
'ID_VENDOR_ID',
'MAJOR',
'MINOR',
'SUBSYSTEM',
'TAGS',
'UDISKS_PRESENTATION_NOPOLICY',
'USEC_INITIALIZED',
'UDISKS_PARTITION_SCHEME',
'UDISKS_PARTITION_SIZE',
'ID_PART_ENTRY_NUMBER',
'ID_PART_ENTRY_SCHEME',
'ID_PART_ENTRY_SIZE',
'ID_PART_ENTRY_TYPE',

    ]
    cmd = "udevadm info -q all -n /dev/%s" % (device)
    (processRc,stdout,stderr) = runpreloadcommand(cmd,10)
    gatheredInfomation = {}
    for line in stdout.split('\n'):
        device_dict = {}
        prefix = line[:3]
        if prefix == 'E: ' :
            postfix = line[3:]
            keyValue = postfix.split('=')
            log.debug (keyValue[0] in eparmas_interesting)
            if not (keyValue[0] in eparmas_interesting):
                log.debug (  line)
                continue
            gatheredInfomation[keyValue[0]] = keyValue[1]

    #log.debug ("doing=%s" % gatheredInfomation)
    return gatheredInfomation
