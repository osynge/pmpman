import logging
import db_devices as model

def initial_data_add_job_state(session,name):
    
    found = session.query(model.job_state).\
            filter(name == model.job_state.name)
    if found.count() == 0:
        state_new = model.job_state()
        state_new.name = name
        session.add(state_new)
        session.commit()
    

def initial_data_add_job_namespace(session,name):
    
    found = session.query(model.job_namespace).\
            filter(name == model.job_namespace.name)
    if found.count() == 0:
        state_new = model.job_namespace()
        state_new.name = name
        session.add(state_new)
        session.commit()
    
    
def initial_data_add_enumerated(session):
    for state in [
                    "create",
                    "pending"
                    "garbidge",
                    "executing",
                    "finished",
                ]:
        initial_data_add_job_state(session,state)
    for job_namespace in [
                    "no_ops",
                    "lsblk_query",
                    "lsblk_read"
                    "udev_query",
                    "udev_read",
                ]:
        initial_data_add_job_namespace(session,job_namespace)
    session.commit()

def job_runner_initial_data_add(session):
    initial_data_add_enumerated(session)
    import db_job_runner

    job_runner_lsblk = db_job_runner.job_runner()
    job_runner_lsblk.job_class = "lsblk_query"
    job_runner_lsblk.uuid_def = "3b201cc5-897c-49c7-87e2-5eaddc31c0c3"
    job_runner_lsblk.name = "lsblk_query"
    job_runner_lsblk.save(session = session)
    
    
    
    job_runner_lsblk_read = db_job_runner.job_runner()
    job_runner_lsblk_read.job_class = "lsblk_read"
    job_runner_lsblk_read.uuid_def = "6d7141d5-e1ee-4ff6-a778-10803521c8a2"
    job_runner_lsblk_read.name = "lsblk_read"
    job_runner_lsblk_read.save(session = session)

    job_runner_udev_query = db_job_runner.job_runner()
    job_runner_udev_query.job_class = "udev_query"
    job_runner_udev_query.uuid_def = "c297b566-089d-4895-a8c2-a9cc37767174"
    job_runner_udev_query.name = "udev_query"
    job_runner_udev_query.save(session = session)

    job_runner_udev_read = db_job_runner.job_runner()
    job_runner_udev_read.job_class = "udev_read"
    job_runner_udev_read.uuid_def = "b9c94c0e-7dc8-4434-9355-e6cb4835fb63"
    job_runner_udev_read.name = "udev_read"
    job_runner_udev_read.save(session = session)

    session.commit()
    
    
    job_runner_lsblk_read.subscribe_add(job_runner_lsblk.uuid_def)
    job_runner_lsblk_read.save(session = session)
    job_runner_udev_query.subscribe_add(job_runner_lsblk_read.uuid_def)
    job_runner_udev_query.save(session = session)
    job_runner_udev_read.subscribe_add(job_runner_udev_query.uuid_def)
    job_runner_udev_read.save(session = session)
    
    session.commit()
    
    job_runner_lsblk.enqueue(session = session)
    session.commit()


def test_CanLaunch(session):
    initial_data_add_enumerated(session)
    import job_manage
    new = job_manage.job_manage()
    new.session = session
    new.create_job_class(name = "lsblk_query")
    new.create_job_class(name = "lsblk_read")
    new.create_job_class(name = "udev_query")
    new.create_job_class(name = "udev_read")
    
    new.create_job_def(
            uuid="3b201cc5-897c-49c7-87e2-5eaddc31c0c3",
            job_class = "lsblk_query",
            cmdln_template = "ls",
            reocuring = 1,
        )
    new.create_job_def(
            uuid="6d7141d5-e1ee-4ff6-a778-10803521c8a2",
            job_class = "lsblk_read",
            cmdln_template = "ls",
            reocuring = 1,
        )
    new.create_job_def(
            uuid="c297b566-089d-4895-a8c2-a9cc37767174",
            job_class = "udev_query",
            cmdln_template = "ls",
            reocuring = 1,
        )
    new.create_job_def(
            uuid="c297b566-089d-4895-a8c2-a9cc37767174",
            job_class = "udev_read",
            cmdln_template = "ls",
            reocuring = 1,
        )
    job_detail = new.get_job_def(uuid = "3b201cc5-897c-49c7-87e2-5eaddc31c0c3")
    job_detail.save()
    queue_count_before = job_detail.queue_count(session= session)
    assert(queue_count_before == 0)
    job_state = job_detail.enqueue(
            session= session,
            uuid_task="3b201cc5-897c-49c7-87e2-5eaddc31c0c3",
            uuid_job="c297b566-089d-4895-a8c2-a9cc37767174",
            cmdln_template="cmdln_template 1",
            reocuring=1,
            job_class="lsblk_query",
            cmdln_paramters="",
            uuid_job_def="c297b566-089d-4895-a8c2-a9cc37767174",

        )
    
