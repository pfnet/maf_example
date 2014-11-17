# Demo: Parameter Tuning Task in Deep Learning

## Overview

In this demo scenario, we solve image classification task with varying Deep Neural Networks(DNNs) and their solvers.

Procedure we take is as follows:

- Generate prototxt’s (which configures DNNs and solvers) with varying parameters
- Evaluate these configuration by
    - training DNNs with image dataset
    - plot transition of train loss during training
    - visualize lowest convolutional layer

We change the following parameters, which amounts to 80 configuration patterns (10 for DNN x 8 for solver)

- For DNN 
    - Convolutional Layer : # of input/output nodes / kernel size
    - Pooling Layer : pooling method (average/max)  / kernel size
- For solver
    -  learning rate / momentum / weight decay

We use [Caffe](http://caffe.berkeleyvision.org) as a DNN library and [CIFAR-10](http://www.cs.toronto.edu/~kriz/cifar.html) as a training dataset.

## Preparation

### Image Dataset Retrieval

After installing Caffe, create dataset with data preparation scripts in Caffe repository.

```
$ cd $CAFFE_ROOT/data/cifar10
$ ./get_cifar10.sh
$  cd $CAFFE_ROOT/examples/cifar10
$ ./create_cifar10.sh
```

Next, get image data for visualization of features.

```
$ cd $DEMO_ROOT/data
$ ./get_image_data.sh
$ tar xvf cifar-10-python.tar.gz
```

### Preparation for wscript

Fill in CAFFE_ROOT in wscript with path to the root directory of Caffe.

## Run Demo

To run demo, execute these commands:

```
$ cd $DEMO_ROOT
$ ./waf configure
$ ./waf build -j1 # (or simply ./waf -j1)
```

To clear generated files do `./waf distclean`