import subprocess
import time
import json
import re
import logging

import udev_query
import datetime


import pmpmanager.db_devices as model
from base_calls import job_exec as bass_job_exec



class job_exec(bass_job_exec):
    def __init__(self):
        bass_job_exec.__init__(self)
        self.remotePrefix = None
        self.log = logging.getLogger("job_exec.lsblk_query")
        self.cmdln_template = "lsblk  --output %s  --pairs"



    

    def run(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session == None:
            session = self.session
        if session == None:
            self.log.error("run:No session set")
            return False

        self.log.debug("command=%s" % ("dsds"))
        
        output = {}
        
        fp = open("/etc/mtab")
        for line in fp.read().split('\n'):
            line_split = line.split(' ')
            if len(line_split) < 4:
                continue
            device = line_split[0]
            mountpoint = line_split[1]
            filesystem = line_split[2]
            option_array = line_split[3].split(",")
            optin_dict = {}
            for item in option_array:
                key_value = item.split("=")
                head = key_value[0]
                tail = str("=").join(key_value[1:])
                if len(tail) == 0:
                    tail = 1
                optin_dict[head] = tail
            
            
            
            line_dict = {
                    "device" : device,
                    "mountpoint" : mountpoint,
                    "filesystem" : filesystem,
                    "options" : optin_dict,
                }
            output[device] = line_dict
            
            
        self.returncode = 0
        self.stdout = ""
        self.outputjson = json.dumps(output,sort_keys=True, indent=4)

        
        
