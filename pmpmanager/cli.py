import logging
import sys
import os
import optparse
from pmpmanager.__version__ import version as pmpman_version
import json
import devices
import lsblk

import db_job_queue
import db_job_runner
# shoudl not be in this function
import pmpmanager.db_devices as model
if __name__ == "__main__":
    main()



class CliInput:
    def __init__(self):
        self.defaults = dict()
        self.callbacks = dict()
        self.log = logging.getLogger("CliInput")
        self.callbacks_set({})

    def process_actions(self):
        output = process_actions(self.defaults,self.callbacks)
        if output == None:
            self.log.error("process_actions:failed")
            return
        self.defaults.update(output)

    def get_parrameters_enviroment(self):
        output = get_parrameters_enviroment(self.defaults)
        if output == None:
            self.log.error("get_parrameters_enviroment:failed")
            return
        self.defaults.update(output)

    def get_parrameters_cli_init(self):
        output = get_parrameters_cli_init(self.defaults)
        actions = output["pmpman.cli.actions"]
        self.log.debug( "pmpman.cli.actions=%s" % actions )
        if "pmpman.cli.actions" in actions:
            pass
        if 'pmpman.action.partition.list' in actions:
            pass

        if output == None:
            self.log.error("get_parrameters_cli_init:failed")
            return
        self.defaults.update(output)

    def callbacks_set(self,update):
        if update == None:
            return
        foundKeys = set(update.keys())
        #self.log.error("dsfsdfsdf=%s" % foundKeys)
        self.callbacks = update

    def callbacks_get(self):
        return self.callbacks

class ProcesHandler:
    def __init__(self,UI = None):
        self.defaults = dict()
        self.log = logging.getLogger("ProcesHandler")
        self.UI = None
        if UI != None:
            self.UI = UI

    def connect_db(self):
        self.database = devices.database_model(self.UI.defaults['pmpman.rdms'])

    def cb_pmpman_action_udev(self,caller=None):
        procerss = 'pmpman.action.udev'
        self.log.info("cb_pmpman_action_udev")
        #output = json.dumps(imagepub.endorserDump(endorserSub),sort_keys=True, indent=4)

        self.connect_db()

    def cb_pmpman_action_list(self,caller=None):
        self.log.debug("cb_pmpman_action_list")




    def cb_pmpman_block_scan(self,caller=None):
        self.log.debug("cb_pmpman_block_scan")
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
        QM = db_job_queue.job_que_man()
        QM.session = self.database.SessionFactory()
        QM.initialise()
        QM.job_persist(job_type = "lsblk_query",
                cmdln_template = "lsblk",
                cmdln_paramters = "{}",
                name = "lsblk",
                uuid = "6d7141d5-e1ee-4ff6-a778-10803521c8a2",
                state = "created"
            )
        QM.job_persist(job_type = "lsblk_query",
                cmdln_template = "udevadm info -q all -n /dev/%s",
                cmdln_paramters = '[ "sdb" ]',
                name = "lsblk_query",
                uuid = "c297b566-089d-4895-a8c2-a9cc37767174",
                state = "created"
            )

        QM.job_persist(job_type = "udev_query",
                cmdln_template = "udevadm info -q all -n /dev/%s",
                cmdln_paramters = '[ "sdb" ]',
                name = "lsblk_query",
                uuid = "b9c94c0e-7dc8-4434-9355-e6cb4835fb63",
                state = "created"
            )




        available = QM.jobtype_available(job_type = "lsblk_query",
                cmdln_template = "udevadm info -q all -n /dev/%s",
                cmdln_paramters = '[ "sdb" ]',
                name = "udev_query",
                session = session,
                state = "created"
            )

        quelength = 100
        while quelength > 0:
            output = QM.queue_dequeue(session = session)
            quelength = 0
        
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

            }
        self.UI.callbacks_set(parmetes)


def main():
    defaults = dict()
    defaults = get_parrameters_enviroment(defaults)
    log = logging.getLogger("cli")

    UI = CliInput()

    UI.defaults = defaults
    UI.get_parrameters_cli_init()
    log = logging.getLogger("cli")
    PH = ProcesHandler(UI)

    PH.Connect()

    UI.process_actions()






def process_actions(defaults,callbacks):
    log = logging.getLogger("process_actions")
    output = dict()
    output.update(defaults)
    actions = output.get("pmpman.cli.actions")
    if actions == None:
        actions = set()
    if len(actions) == 0:
        log.warning('No actions selected')
    #log.debug("actions=%s" % (actions))
    #log.debug("callbacks=%s" % (callbacks))
    for match_tuple in actions.intersection(callbacks.keys()):
        for i in range ( len(callbacks[match_tuple])):
            callback = callbacks[match_tuple][i].get('callback')
            callback(caller = defaults)

    #if 'endorser_show' in actions:
    #    json_output = json.dumps(imagepub.endorserDump(endorserSub),sort_keys=True, indent=4)
    #    if json_output != None:
    #        print json_output
    return output

def get_parrameters_enviroment(defaults):
    output = dict()
    output.update(defaults)
    if 'PMPMAN_LOG_CONF' in os.environ:
        output['pmpman.logcfg'] = str(os.environ['PMPMAN_LOG_CONF'])
    if 'PMPMAN_RDBMS' in os.environ:
        output['pmpman.rdms'] = str(os.environ['PMPMAN_RDBMS'])
    if 'PMPMAN_CFG' in os.environ:
        output['pmpman.path.cfg'] = str(os.environ['PMPMAN_CFG'])
    if 'HOME' in os.environ:
        output['pmpman.path.home'] = str(os.environ['HOME'])

    return output

def get_parrameters_cli_init(defaults):
    output = dict()
    output.update(defaults)
    """Runs program and handles command line options"""
    p = optparse.OptionParser(version = "%prog " + pmpman_version)
    p.add_option('-d', '--database', action ='store', help='Database conection string')
    p.add_option('-L', '--logcfg', action ='store',help='Logfile configuration file.', metavar='CFG_LOGFILE')
    p.add_option('-v', '--verbose', action ='count',help='Change global log level, increasing log output.', metavar='LOGFILE')
    p.add_option('-q', '--quiet', action ='count',help='Change global log level, decreasing log output.', metavar='LOGFILE')
    p.add_option('-C', '--config-file', action ='store',help='Configuration file.', metavar='CFG_FILE')
    p.add_option('--mark-udev', action ='store',help='Called by udev $name')
    p.add_option('--list-partitions', action ='store_true',help='Called by udev $name')
    p.add_option('--block-list', action ='store_true',help='Scan All Partitions')
    p.add_option('--block-scan', action ='store_true',help='Scan All Partitions')


    actions = set()
    requires = set()
    options, arguments = p.parse_args()
    # Set up log file
    LoggingLevel = logging.WARNING
    LoggingLevelCounter = 2
    if options.verbose:
        LoggingLevelCounter = LoggingLevelCounter - options.verbose
        if options.verbose == 1:
            LoggingLevel = logging.INFO
        if options.verbose == 2:
            LoggingLevel = logging.DEBUG
    if options.quiet:
        LoggingLevelCounter = LoggingLevelCounter + options.quiet
    if LoggingLevelCounter <= 0:
        LoggingLevel = logging.DEBUG
    if LoggingLevelCounter == 1:
        LoggingLevel = logging.INFO
    if LoggingLevelCounter == 2:
        LoggingLevel = logging.WARNING
    if LoggingLevelCounter == 3:
        LoggingLevel = logging.ERROR
    if LoggingLevelCounter == 4:
        LoggingLevel = logging.FATAL
    if LoggingLevelCounter >= 5:
        LoggingLevel = logging.CRITICAL
    output["pmpman.logging.level"] = LoggingLevel
    if options.logcfg:
        output['pmpman.path.cfg'] = options.logcfg
    if defaults.get('pmpman.path.cfg') != None:
        if os.path.isfile(str(options.log_config)):
            logging.config.fileConfig(options.log_config)
        else:
            logging.basicConfig(level=LoggingLevel)
            log = logging.getLogger("main")
            log.error("Logfile configuration file '%s' was not found." % (options.log_config))
            sys.exit(1)
    else:
        output['pmpman.path.cfg'] = None
        logging.basicConfig(level=LoggingLevel)

    log = logging.getLogger("main")
    if options.mark_udev:
        actions.add('pmpman.action.udev')
        output["pmpman.udev.partition"] = options.mark_udev
    if options.mark_udev:
        actions.add('pmpman.action.udev')
        output["pmpman.udev.partition"] = options.mark_udev

    if options.list_partitions:
        actions.add('pmpman.action.partition.list')


    if options.block_list:
        actions.add('pmpman.action.block.list')

    if options.block_scan:
        actions.add('pmpman.action.block.scan')

    output["pmpman.cli.actions"] = actions

    if options.database:
        output['pmpman.rdms'] = options.database

    if output.get('pmpman.rdms') == None:
        output['pmpman.rdms'] = 'sqlite:///pmpman.db'
        log.info("Defaulting DB connection to '%s'" % (output['pmpman.rdms']))
    return output
