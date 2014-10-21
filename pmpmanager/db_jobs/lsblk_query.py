import subprocess
import time
import json
import re
import logging

import udev_query
import datetime


import pmpmanager.db_devices as model
from base_calls import job_runner as bass_job_runner

lsblk_wantedFields = ["NAME","KNAME","MOUNTPOINT","PARTUUID","SERIAL","FSTYPE","RM","SIZE","FSTYPE","UUID","OWNER","GROUP","MODE","WWN","VENDOR","MAJ:MIN"]
cmdln = "lsblk  --output %s  --pairs" % (",".join(lsblk_wantedFields))


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
        bass_job_runner.__init__(self)
        self.remotePrefix = None
        self.log = logging.getLogger("job_runner.lsblk_query")
        self.cmdln_template = "lsblk  --output %s  --pairs"



    

    def run(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            log.warning("job_def_Add missing name")
            return



        #log.debug("command=%s" % (command))

        processRc,stdout,stderr = self.execuet_cmdln(cmdln = self.cmdln, timeout=10)
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
        self.returncode = processRc
        self.stdout = stderr
        self.outputjson = json.dumps(output,sort_keys=True, indent=4)

        self.triggers = json.dumps(["lsblk_read"],sort_keys=True, indent=4)

        paramters = []
        for key in output.keys():
            paramters.append(output[key])
        self.trig_parameters = json.dumps(paramters,sort_keys=True, indent=4)

