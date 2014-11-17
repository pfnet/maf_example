import maflib.util
import string
import json

@maflib.util.rule
def fill_template(task):
    template = string.Template(task.inputs[0].read())
    task.outputs[0].write(template.safe_substitute(task.parameter))

@maflib.util.rule
def generate_datalayer(task):
    fill_template(task)

@maflib.util.rule
def generate_net(task):
    fill_template(task)
    
@maflib.util.rule
def generate_solver(task):
    template = string.Template(task.inputs[0].read())
    parameter = {'net' : task.inputs[1].abspath(),
                 'snapshot_prefix' : task.outputs[1].abspath()
             }
    template = string.Template(template.safe_substitute(parameter))
    task.outputs[0].write(template.safe_substitute(task.parameter))
    task.outputs[1].write('done', 'w')
