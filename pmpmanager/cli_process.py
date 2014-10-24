import logging
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

import db_devices as model

import job_queue_manager
import pmpmanager.initialise_db as  devices

import pmpmanager.job_manage as job_manage

import job_queue_manager
import uuid
from dirty_parser import dirty_parser

class ProcesHandler:
    def __init__(self,UI = None):
        self.defaults = dict()
        self.log = logging.getLogger("ProcesHandler")
        self.UI = None
        if UI != None:
            self.UI = UI

    def connect_db(self):
        #self.database = devices.database_model(self.UI.defaults['pmpman.rdms'])
        #print self.UI.defaults['pmpman.rdms']
        pass

    def cb_pmpman_action_udev(self,caller=None):
        procerss = 'pmpman.action.udev'
        self.log.info("cb_pmpman_action_udev")
        #output = json.dumps(imagepub.endorserDump(endorserSub),sort_keys=True, indent=4)

        self.connect_db()

    def cb_pmpman_action_list(self,caller=None):
        self.log.debug("cb_pmpman_action_list=started")

        self.engine = create_engine(self.UI.defaults['pmpman.rdms'], echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        session = self.SessionFactory()
        devices.test_CanLaunch(session)

        JM = job_manage.job_manage()
        JM.session = session
        job_template = JM.get_job_def(uuid = "3b201cc5-897c-49c7-87e2-5eaddc31c0c3")

        new_uuid1 = str(uuid.uuid1())
        new_uuid2 = str(uuid.uuid1())
        new_uuid3 = str(uuid.uuid1())
        job_state = job_template.enqueue(
                session= session,
                uuid_task=new_uuid2,
                uuid_job=new_uuid3,
                cmdln_template="cmdln_template 1",
                reocuring=1,
                job_class="lsblk_query",
                cmdln_paramters="",
                uuid_job_def=new_uuid3
            )

        job_template.run(new_uuid1)
        dirty_parser(session)
        self.log.debug("queue_count=%s" % (job_template.queue_count()))
        QM = job_queue_manager.job_que_man()
        QM.session = session

        quelength = QM.queue_length(session = session)
        while quelength > 0:
            self.log.debug("cb_pmpman_block_scan:finished=%s" % (quelength))
            output = QM.queue_dequeue(session = session)
            quelength = quelength = QM.queue_length(session = session)
            time.sleep(10)
        self.log.debug("cb_pmpman_action_list")


    def cb_pmpman_action_list_old(self,caller=None):
        self.log.debug("cb_pmpman_action_list=started")
        self.connect_db()
        session = self.database.Session()

        newone = db_job_runner.job_runner()
        newone.session = session
        uuid_req = str(uuid.uuid1())
        uuid_execution = str(uuid.uuid1())
        self.log.debug("uuid_req=%s" % (uuid_req))
        self.log.debug("uuid_execution=%s" % (uuid_execution))

        newone.load(session = session,
            uuid_def = "3b201cc5-897c-49c7-87e2-5eaddc31c0c3",
            uuid_req = uuid_req,
            uuid_execution = uuid_execution,
            )
        newone.enqueue(session = session)
        newone.load(session = session,
            uuid_def = "6d7141d5-e1ee-4ff6-a778-10803521c8a2",
            uuid_execution = str(uuid.uuid1()),
            uuid_req = str(uuid.uuid1()),
            )
        newone.enqueue(session = session,uuid_req = uuid.uuid1())
        newone.load(session = session,
            uuid_def = "c297b566-089d-4895-a8c2-a9cc37767174",
            uuid_execution = str(uuid.uuid1()),
            uuid_req = str(uuid.uuid1()),
            )

        newone.enqueue(session = session,uuid_req = uuid.uuid1())
        newone.load(session = session,
            uuid_def = "b9c94c0e-7dc8-4434-9355-e6cb4835fb63",
            uuid_execution = str(uuid.uuid1()),
            uuid_req = str(uuid.uuid1()),
            )
        newone.enqueue(session = session,uuid_req = uuid.uuid1())


        QM = job_queue_manager.job_que_man()
        QM.session = session

        quelength = QM.queue_length(session = session)
        while quelength > 0:
            self.log.debug("cb_pmpman_block_scan:finished=%s" % (quelength))
            output = QM.queue_dequeue(session = session)
            quelength = quelength = QM.queue_length(session = session)
            time.sleep(10)
        self.log.debug("cb_pmpman_action_list")

    def cb_pmpman_block_scan(self,caller=None):
        self.log.debug("cb_pmpman_block_scan:ended")
        self.connect_db()
        session = self.database.Session()
        #lsblk.updatdatabase(session)
        #self.database.job_namespace_Add(update_type="lsblk",)
        #self.database.job_namespace_Add(update_type="udevadm_info")
        #self.database.job_namespace_Run()
        #self.database.job_def_Run()
        #self.database.job_execution_Run()
        #self.database.job_def_Add(update_type="udevadm_info",
        #   cammand_line = "" )

        #self.database.job_def_Run(update_type="lsblk")
        #self.database.job_execution_Run(update_type="lsblk")
        QM = job_queue_manager.job_que_man()
        QM.session = session
        session = self.database.Session()






        available = QM.jobtype_available(job_type = "lsblk_query",
                cmdln_template = "udevadm info -q all -n /dev/%s",
                cmdln_paramters = '[ "sdb" ]',
                name = "udev_query",
                session = session,
                state = "created"
            )

        quelength = QM.queue_length(session = session)

        while quelength > 0:
            self.log.debug("cb_pmpman_block_scan:finished=%s" % (quelength))
            output = QM.queue_dequeue(session = session)
            quelength = quelength = QM.queue_length(session = session)
            time.sleep(10)
        self.log.debug("cb_pmpman_block_scan:finished")
    def cb_pmpman_block_list(self,caller=None):
        self.log.debug("cb_pmpman_block_list")
        self.connect_db()
        session = self.database.Session()

        find_job_def = session.query(model.Block)


        if find_job_def.count() == 0:
            self.log.info("No blocks found")




    def Connect(self):
        """This function sets callbacks"""

        parmetes =  {
            'pmpman.action.udev' : [ { 'callback' : self.cb_pmpman_action_udev } ],
            'pmpman.action.partition.list' : [ { 'callback' : self.cb_pmpman_action_list } ],
            'pmpman.action.block.list' : [ { 'callback' : self.cb_pmpman_block_list } ],
            'pmpman.action.block.scan' : [ { 'callback' : self.cb_pmpman_block_scan } ],
            'pmpman.action.queue.display' : [ { 'callback' : self.cb_pmpman_block_scan } ],


            }
        self.UI.callbacks_set(parmetes)

