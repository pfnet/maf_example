import maflib.util
import numpy as np
import matplotlib.pyplot as plt
import caffe
import cPickle

def vis_square(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()
    
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    return data

def write(data, out_file):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(data)
    plt.savefig(out_file)

@maflib.util.rule
def classify(task):
    model_file = task.inputs[0].abspath()
    pretrained_file = '%s_iter_%d.caffemodel' % (task.inputs[1].abspath(), task.parameter['max_iter'])
    net = caffe.Classifier(model_file, pretrained_file)
    net.set_phase_test()
    net.set_mode_cpu()
    with open(task.parameter['image_file'], 'rb') as f:
        data = map(lambda x: x.reshape((32, 32, 3)), cPickle.load(f)['data'][:20])
    net.predict(data)
    d = net.params['conv1'][0].data.transpose(0, 2, 3, 1)
    dd = vis_square(d)
    write(dd, task.outputs[0].abspath())
