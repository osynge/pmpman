import logging

from base_calls import job_runner as bass_job_runner


class job_runner(bass_job_runner):
    def __init__(self):
        self.log = logging.getLogger("job_runner.udev_read")
    def run(self, *args, **kwargs):
        pass

