

def validate(work):
    if not work.has_key('pmpman'):
        return False
    return True
    

def get_session_type(work):
    if not work.has_key('pmpman'):
        return None

    if not work['pmpman'].has_key('msg'):
        return None
    return work['pmpman']['msg']
    
    
    
def get_session_socket(work):
    if not work.has_key('pmpman'):
        return None
    if not work['pmpman'].has_key('parmaters'):
        return None    
    if not work['pmpman']['parmaters'].has_key('recives'):
        return None
    return work['pmpman']['parmaters']['recives']




def get_sessionid(work):
    if not work.has_key('pmpman'):
        return None

    if not work['pmpman'].has_key('session_id'):
        return None
    return work['pmpman']['session_id']


def get_jobid(work):
    if not work.has_key('pmpman'):
        return None

    if not work['pmpman'].has_key('jobid'):
        return None
    return work['pmpman']['jobid']



