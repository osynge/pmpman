import time
import zmq
import random

import uuid
import msg_utils
address = "tcp://127.0.0.1:5557"
address = "ipc:///tmp/feeds/0"


import tempfile
from sqlalchemy import create_engine

import db_devices as model

from sqlalchemy.orm import sessionmaker

import initialise_db


time_format_definition = "%Y-%m-%dT%H:%M:%SZ"

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime
import datetime

def req_session_id_set(zmq_socket,workerId,workerType,workerdescription):
    
    work_message = { 'pmpman' : { 'msg' :'req_session_id',
        'parmaters' : {   
            'workerId' : workerId ,
            'type' : workerType,
            'params' : workerdescription,
            'recives' : zmq_socket_inbound
            }
        }}
    zmq_socket.send_json(work_message)


def req_job_id_set(zmq_socket,workerId,workerType,workerdescription):
    
    work_message = { 'pmpman' : { 'msg' :'req_session_id',
        'parmaters' : {   
            'jobId' : workerId ,
            'type' : workerType,
            'params' : workerdescription,
            'recives' : zmq_socket_inbound
            }
        }}
    zmq_socket.send_json(work_message)


class two_process(object):
    def __init__(self):
        self.processId = str(uuid.uuid1())
        
    def _gen_base_msg(self):
        msguuid = str(uuid.uuid1())
        return {
            'pmpman' : {
                'msgid' : self.processId,
                'msg_uuid' : msguuid,
                'params' : {},
            }
        }
    def process_req_job_id(self,message):
        pass
    
    def process_req_session_id(self,message):
        pass
    
    
    def process_req_repository(self,message):
        pass

    def process_req_file(self,message):
        pass

    def process_req_checksum(self,message):
        pass
    
    def execute(self,params):
        if acrgs == "req_job_id":
            return self.process_req_job_id(params)
        if acrgs == "req_session_id":
            return self.process_req_session_id(params)
    
    def get_types(self):
        
        return set( ["req_file",
            "req_repository",
            "req_checksum",
            "process_req_session_id",
            "process_req_checksum" ])


class two_process_implementation(two_process):
    def __init__(self,db):
        two_process.__init__(self)
        self._db = db

    
    def process_req_job_id(self,message):
        print "process_req_job_id.in=%s" % (message)
        session_id_liat = msg_utils.get_sessionid(message)
        if len(session_id_liat) == 0:
            print "nosession_id"
            return None
            session_socket = get_session_socket(message)
            
            
        #socket = msg_utils.get_session_socket(message)

        #consumer_sender = self.context.socket(zmq.PUSH)
        #consumer_sender.connect(socket)  
        #output = self._gen_base_msg()
                
        #consumer_sender.send_json(output)
        
        
        output = self._gen_base_msg()
        session = self._db.SessionFactory()
        for session_id in session_id_liat:
            query_client = session.query(model.client).\
                    filter(model.client.uuid  == session_id)
            if query_client.count() == 0:
                newclient = model.client()
                uuid_str = str(uuid.uuid1())
                newclient.uuid = uuid_str
                session.add(newclient)
                session.commit()
                query_client = session.query(model.client).\
                    filter(session_id == model.client.uuid)
            
            output['pmpman']['results'] = []
            for client in query_client:
                content = {}
                content['sss'] = content.uuid
                output['pmpman']['results'].append(content)
            
        
        return output
   
    def process_req_session_id(self,message):
        sessionsocket_name = msg_utils.get_session_socket(message)
        #print work
        if None == sessionsocket_name:
            return
        session = self._db.SessionFactory()
        results = []
        query_client_cross = session.query(model.client, model.client_job).\
            filter(model.client.id == model.client_job.fk_client).\
            filter(model.client.client_sock == sessionsocket_name)
        if query_client_cross.count() == 0:
            query_client = session.query(model.client).\
                filter(model.client.client_sock == sessionsocket_name)
            if query_client.count() == 0:
                client_details = model.client()
                client_details.uuid = str(uuid.uuid1())
                client_details.client_job_latest = None
                client_details.client_sock = sessionsocket_name
                session.add(client_details)
                session.commit()
                query_client = session.query(model.client).\
                    filter(model.client.client_sock == sessionsocket_name)  
            for client in query_client:
                query_job =  session.query(model.client_job).\
                    filter(model.client.id == model.client_job.fk_client).\
                    filter(model.client.client_sock == sessionsocket_name)
                session_details = model.client_job()
                session_details.fk_client = client.id
                session_details.uuid = str(uuid.uuid1())
                session_details.client_job_latest = None
                session_details.created = datetime.datetime.now()
                session_details.expires = datetime.datetime.now()
                session_details.session_id = str(uuid.uuid1())
                session.add(session_details)
                break
        session.commit()
        results = []
        
        query_client_cross = session.query(model.client, model.client_job).\
            filter(model.client.id == model.client_job.fk_client).\
            filter(model.client.client_sock == sessionsocket_name)
        for client_cross in query_client_cross:
            client, client_job = client_cross
            details = {
                "id_client" : client.uuid,
                "created" : client_job.created.strftime(time_format_definition),
                "expires" :client_job.expires.strftime(time_format_definition),
                "id_session" : client_job.session_id,
                "client_sock" : client.client_sock
            }
            results.append(details)
        
        output = self._gen_base_msg()
        output['pmpman'] = {}
        output['pmpman']['params'] = {}
        output['pmpman']['params']['results'] = results
        
        
        session_id = msg_utils.get_sessionid(message)
        session_details = None
        if session_id == None:
            session_details_uuid = str(uuid.uuid1())
            session_details = model.client()
            session_details.uuid = session_details_uuid
        
        print output
        return output
    
    
   
    def execute(self,acrgs,params):
        #print acrgs
        if acrgs == "req_job_id":
            return self.process_req_job_id(params)
        if acrgs == "req_session_id":
            return self.process_req_session_id(params)
        print "miss"
        
class two_connection(object):
    def __init__(self,context):
        self.context = context
        self.handler = two_process()
    
    def handler_set(self,handler):
        self.handler = handler
        rubbish = """
        caller = { 'req_job_id' : self.handler.process_req_job_id,
            'req_session_id' : self.handler.process_req_session_id,
            'req_checksum' : self.handler.process_req_checksum,
            'req_file' : self.handler.process_req_file,
            
            }
        """
        
        
        
    def process_req_job_id(self,message):
        #print "process_req_job_id.in=%s" % (message)
        session_id = msg_utils.get_sessionid(message)
        if session_id == None:
            return
        socket = msg_utils.get_session_socket(message)

        output = self._gen_base_msg()
        new_job_id = str(uuid.uuid1())
        output['pmpman'] = {}
        output['pmpman']['params'] = {}

        output['pmpman']['params']['new_job_id'] = new_job_id

        return output



    def execute(self,work):
    
        if self.handler == None:
            return
        acrgument = msg_utils.get_session_type(work)
        output = self.handler.execute(acrgument,work)
        
        print "argumenty =" , acrgument
        print "work =" , work
        print "zzzzzzoutput =" , output
        
        return output

    def consumer(self):

        # recieve work
        consumer_receiver = self.context.socket(zmq.PULL)
        consumer_receiver.connect(address)
        # send work


        sessionsocket_name = None
        while True:
            work = consumer_receiver.recv_json()
            print work
            if not msg_utils.validate(work):
                continue

            message = self.execute(work)
            socket = msg_utils.get_session_socket(work)
            workout = self.execute(work)
            consumer_sender = self.context.socket(zmq.PUSH)
            consumer_sender.connect(socket)
            print workout
            consumer_sender.send_json(workout)
            print workout


class dbconnection(object):
    def dbconnectionstring_set_random(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        self.databaseConnectionString = "sqlite:///%s" % (f.name)
        
    def setup(self):
        self.engine = create_engine(self.databaseConnectionString, echo=False)
        model.init(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)
        initialise_db.initial_data_add_enumerated(self.SessionFactory())
    
    



        
def consumer():


    db = dbconnection()
    db.dbconnectionstring_set_random()
    db.setup()

    consumer_id = random.randrange(1,10005)
    print "I am consumer #%s" % (consumer_id)
    context = zmq.Context()
    
    foo = two_connection(context)
    bar = two_process_implementation(db)
    foo.handler_set(bar)
    foo.consumer()
    
        

consumer()
