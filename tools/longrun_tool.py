import time, uuid
RUN_STORE = {}
def start_long_op(op_name, params):
    op_id = str(uuid.uuid4())
    RUN_STORE[op_id] = {"status":"running","name":op_name,"started":time.time(),"params":params}
    # simulate background by setting a result later (or you can spawn thread)
    return {"op_id":op_id,"status":"running"}

def check_status(op_id):
    return RUN_STORE.get(op_id, {"status":"unknown"})
