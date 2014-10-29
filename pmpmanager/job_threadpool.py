import socket
import httplib, urllib
import sys, traceback
from threading import *
import logging
from Queue import Queue, Empty
import exceptions

import sys
import time

if float(sys.version[:3]) >= 2.6:
    import json
else:
    # python 2.4 or 2.5 can also import simplejson
    # as working alternative to the json included.
    import simplejson as json



class thread_job_worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.callbacks = { 'task_done' : {}}
        self.daemon = True
        self.start()
        self.connectionString = None
        self.log = logging.getLogger("thread_job_worker")
        self.conn = None

    def cbAddTaskDone(self,funct):
        self.callbacks['task_done'][funct] = 1

    def taskDone(self,request):
        self.tasks.task_done()
        self.log.debug( 'taskDone')
        for func in self.callbacks['task_done']:
            func(request)
        # Now process nicely
        return


    def processRequest(self,request):
        time.sleep(1)
        return

    def run(self):
        while self.daemon:
            request = self.tasks.get()
            self.log.debug('Running')
            reponce = self.processRequest(request)
            if reponce != None:
                request['responce'] = reponce

            self.taskDone(request)

    def ConnectionSet(self,connectionStr):
        #print "connectionStr", connectionStr
        Changed =  False
        if not hasattr(self,'connectionString'):
            Changed =  True
            self.connectionString = connectionStr
        if self.connectionString != connectionStr:
            Changed =  True
            self.connectionString = connectionStr
        if not hasattr(self,'conn'):
            Changed =  True
        elif self.conn == None:
            Changed =  True
        self.conn = None




class threadpool_jobs:
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, num_threads = 10):
        self.log = logging.getLogger("threadpool_jobs")
        self.tasks = Queue(num_threads)
        self.preTasks = Queue()
        self.arrayOfthread_job_worker = []
        self.taskCacheRunning = {}
        self.preTaskCache = {}
        self.callbacks = {
                "messagesToProcess" : {},
            }
        self.taskCacheFinished = {}
        self.postTasks = Queue()
        self.blockedMessages = {}
        for item in range(num_threads):
            new = thread_job_worker(self.tasks)
            new.cbAddTaskDone(self.handleTaskDoneByThread)
            self.arrayOfthread_job_worker.append(new)

    def cbAddOnMessagesToProcess(self,function):

        self.callbacks['messagesToProcess'][function] = 1
    def cbDoOnMessagesToProcess(self):
        for item in self.callbacks["messagesToProcess"]:
            item(self)
    def handleTaskDoneByThread(self,request):
        self.log.debug('handleTaskDoneByThread')
        msgHash = request['params'].__hash__()
        if msgHash in self.taskCacheRunning.keys():
            del(self.taskCacheRunning[msgHash])
        #self.log.debug(request)
        if not 'responce' in request.keys():
            self.log.error('no reponce')
            self.log.debug("request=%s" % (request))
            # we will requeue the responce
            if not 'retries' in request.keys():
                request['retries'] = 0
            request['retries'] += 1
            if request['retries'] > 2:
                self.blockedMessages[msgHash] = request
                return
            if msgHash in self.preTaskCache.keys():
                self.preTaskCache[msgHash]['retries'] = request['retries']
            else:
                self.preTaskCache[msgHash] = request
            self.preTasks.put(request)
            return
        self.taskCacheFinished[msgHash] = request
        self.postTasks.put(msgHash)
        self.cbDoOnMessagesToProcess()

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.log.error("Wait for completion of all the tasks in the queue")
        self.tasks.join()

    def SendMessage(self,func,message, *args, **kargs):
        #Sends a message now without Queuing
        #for a aproved thread
        request = {
            'function' : func,
            'params' : message,
            'args' : args,
            'kargs' : kargs,
        }
        msgHash = request['params'].__hash__()
        if msgHash in self.taskCacheRunning.keys():
            self.log.error("SendMessage Overwriting task")
        self.taskCacheRunning[msgHash] = request
        self.tasks.put(request)

        self.QueueProcessPreTask()

    def QueueProcessPreTask(self):
        # For calling to place messages on
        #self.log.debug( 'self.preTasks.qsize=%s' % (   self.preTasks.qsize()))
        while True:
            try:
                request = self.preTasks.get_nowait()
            except Empty:
                break

            msgHash = request['params'].__hash__()
            self.taskCacheRunning[msgHash] = request
            if msgHash in self.preTaskCache.keys():
                del self.preTaskCache[msgHash]
            #print request
            self.tasks.put(request)
            self.preTasks.task_done()
        #self.log.debug('self.preTasks.qsize=%s' % (   self.preTasks.qsize()))
        #self.log.debug('self.tasks.qsize=%s' % (   self.tasks.qsize()))

    def QueueProcessResponces(self):
        # To be processed by external thead
        counter = 0
        #self.log.debug('self.postTasks.qsize=%s' % (  self.postTasks.qsize()))
        while True:
            try:
                msgHash = self.postTasks.get_nowait()
            except Empty:
                break
            if not msgHash in self.taskCacheFinished.keys():
                self.postTasks.task_done()
                continue

            func = self.taskCacheFinished[msgHash]['function']
            params = self.taskCacheFinished[msgHash]['params']
            args = self.taskCacheFinished[msgHash]['args']
            kargs = self.taskCacheFinished[msgHash]['kargs']
            rep = self.taskCacheFinished[msgHash]['responce']
            if func != None:
                func(rep,params,*args, **kargs)
            #try: func(rep)
            #except Exception, e:
            #    print e
            #    #traceback.print_tb(e, limit=1, file=sys.stdout)

            del(self.taskCacheFinished[msgHash])
            self.postTasks.task_done()
        #self.log.debug('self.postTasks.qsize=%s' % ( self.postTasks.qsize())   )
    def QueueProcessAddMessage(self,func,message, *args, **kargs):
        messageDict = {}
        if message.__hash__() in self.preTaskCache.keys():
            self.log.debug('preTaskCache dedupe is working')
            return
        request = {
            'function' : func,
            'params' : message,
            'args' : args,
            'kargs' : kargs,
        }
        self.preTaskCache[message.__hash__()] = request
        self.preTasks.put(request)
        #self.log.debug('adding self.preTasks.qsize=%s' % (   self.preTasks.qsize()))




def testcbDone(one):
    print one

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import time
    log = logging.getLogger("main")
    model.host.set('mini')
    poool = sConTPool(model)
    msg = {
            "method": "slim.request",
            "params": [
                "-",
                [
                    "player",
                    "count",
                    "?"
                ]
            ]
        }

    poool.SendMessage(testcbDone,msg)

    log.error('self.tasks.qsize=%s' % (  poool.tasks.qsize()))
    time.sleep(20)

