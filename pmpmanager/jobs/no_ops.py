import logging

from base_calls import job_exec as bass_job_exec


class job_exec(bass_job_exec):
    def __init__(self):
        self.log = logging.getLogger("job_exec.udev_read")
    def run(self, *args, **kwargs):
        pass
    
