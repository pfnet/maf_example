import maflib
import matplotlib.pyplot as plt
import json

@maflib.plot.plot_by
def plot(figure, data, parameter):
    axes = figure.add_subplot(111)

    axes.set_xlabel('iteratiron')
    axes.set_ylabel('loss')

    key_name=('base_lr', 'momentum', 'weight_decay')
    key2data = data.get_data_2d('iteration', 'loss', key=key_name)
    for key in sorted(key2data):
        iteration, loss =  key2data[key]
        axes.plot(iteration, loss, label='%s=%s' % (str(key_name), str(key)))
    axes.legend(loc='upper right', fontsize=9)
    plt.close()
