import maflib
import json
import re

@maflib.util.rule
def extract_loss(task):
    ret = []
    for line in task.inputs[0].read().split('\n'):
        m = re.match(r'I.*solver.cpp:191] Iteration ([0-9]*), loss = ([0-9\.]*).*', line)
        if m is None: continue
        iter_num, loss = int(m.group(1)), float(m.group(2))
        ret.append({'iteration' : iter_num, 'loss' : loss})
    task.outputs[0].write(json.dumps(ret))
