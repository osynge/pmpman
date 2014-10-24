import logging
import json


import subprocess
import time

import logging

from base_calls import job_runner as bass_job_runner

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



def Property(func):
    return property(**func())


class job_runner(bass_job_runner):
    def __init__(self):
        self.remotePrefix = None
        self.log = logging.getLogger("job_runner.udev_query")
        self.cmdln_template = "udevadm info -q all -n /dev/%s"
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
        cmdln = kwargs.get('cmdln', None)
        self.log.debug("self.cmdln.=%s" % cmdln)
        self.log.debug("self.job_class=%s" % self.job_class)
        self.trig_parameters = json.dumps([],sort_keys=True, indent=4)

        session = kwargs.get('session', None)
        if session == None:
            log.warning("Session not parsed")
            return
        self.log.debug("self.job_class=%s" % self.job_class)
        output = []
        #print self.cmdln
        self.returncode = 0
        self.stdout = ""
        self.outputjson = json.dumps(output,sort_keys=True, indent=4)
        self.triggers = json.dumps(["udev_read"],sort_keys=True, indent=4)
        paramters = []
        for key in output:
            paramters.append(output[key])
        self.trig_parameters = json.dumps(paramters,sort_keys=True, indent=4)

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
        device = "sdb"
        cmd = "udevadm info -q all -n /dev/%s" % (device)
        (processRc,stdout,stderr) = self.execuet_cmdln(cmdln = cmd)
        gatheredInfomation = {}
        for line in stdout.split('\n'):
            device_dict = {}
            prefix = line[:3]
            if prefix == 'E: ' :
                postfix = line[3:]
                keyValue = postfix.split('=')
                #log.debug (keyValue[0] in eparmas_interesting)
                if not (keyValue[0] in eparmas_interesting):
                    log.debug (  line)
                    continue
                gatheredInfomation[keyValue[0]] = keyValue[1]

        #log.debug ("doing=%s" % gatheredInfomation)
        self.outputjson = json.dumps(gatheredInfomation,sort_keys=True, indent=4)
        return gatheredInfomation



    def cmdln_gen(self,paramters):
        return string.Template(self.cmdln_template).substitute()

