import logging
import sys
import os
import optparse
from pmpmanager.__version__ import version as pmpman_version
import json

import lsblk
import time

import pmpmanager.db_devices as model
if __name__ == "__main__":
    main()

import uuid

#import queue_display

import pmpmanager.initialise_db as  devices

from cli_process import ProcesHandler

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
    p.add_option('--add-filestore', action ='store_true',help='List all known instalations')
    p.add_option('--list-partitions', action ='store_true',help='Called by udev $name')
    p.add_option('--list-filestore', action ='store_true',help='List all known instalations')
    p.add_option('--block-list', action ='store_true',help='Scan All Partitions')
    p.add_option('--block-scan', action ='store_true',help='Scan All Partitions')
    p.add_option('--queue-display', action ='store_true',help='Scan All Partitions')



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

    if options.add_filestore:
        actions.add('pmpman.action.filestore.add')

    if options.list_partitions:
        actions.add('pmpman.action.partition.list')


    if options.block_list:
        actions.add('pmpman.action.block.list')
    if options.list_filestore:
        actions.add('pmpman.action.filestore.list')

    if options.block_scan:
        actions.add('pmpman.action.block.scan')
    if options.queue_display:
        actions.add('pmpman.action.queue.display')

    output["pmpman.cli.actions"] = actions

    if options.database:
        output['pmpman.rdms'] = options.database

    if output.get('pmpman.rdms') == None:
        output['pmpman.rdms'] = 'sqlite:///pmpman.db'
        log.info("Defaulting DB connection to '%s'" % (output['pmpman.rdms']))
    return output
