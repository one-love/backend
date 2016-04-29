from threading import Thread
from celery.result import AsyncResult


thread = None


def my_monitor():
    from .. import current_app
    celery = current_app.celery
    state = celery.events.State()

    def task_state_changed(event):
        from .. import current_app
        state.event(event)
        task = AsyncResult(event['uuid'])
        current_app.socketio.emit(
            'task',
            {
                'id': task.id,
                'status': task.status,
            },
            namespace='/onelove',
        )

    def ansible_log(event):
        from .. import current_app
        state.event(event)
        task = AsyncResult(event['uuid'])
        current_app.socketio.emit(
            'task',
            {
                'id': task.id,
                'status': task.status,
                'task': event['task'],
                'host': event['host'],
            },
            namespace='/onelove',
        )

    with celery.connection() as connection:
        recv = celery.events.Receiver(
            connection,
            handlers={
                'task-started': task_state_changed,
                'task-succeeded': task_state_changed,
                'task-failed': task_state_changed,
                'ansible-log': ansible_log,
                '*': state.event,
            },
            app=celery,
        )
        recv.capture(limit=None, timeout=None, wakeup=True)


def create_monitor():
    global thread
    if thread is None:
        thread = Thread(target=my_monitor)
        thread.daemon = True
        thread.start()
