# Demo: Cross Validation Task with LIBLINEAR

## Overview

In this demo scenario, we perform a series of procedures which is typical in machine learning.

- Split dataset (we use [svmguide3](http://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/svmguide3) ) into 10 pieces
- With varying training methods and cost functions which differ in regularization, 
    - execute one versus rest for each part of dataset with LIBLINEAR
    - calculate average accuracy of 10-fold cross validation
    - plot accuracy with respect to cost function

## Run Demo

To run demo, execute these commands:

```
$ cd $DEMO_ROOT
$ ./waf configure
$ ./waf build # or simply ./waf
```

To clear generated files do `./waf distclean`