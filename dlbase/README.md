# DeepLearning Container Image Base

This directory is an attempt to build a docker image equivalent to
Google's Deep Learning Container Image
https://cloud.google.com/deep-learning-containers/docs/choosing-container
but customized in the ways we need.

In particular, we want to install python3.9 since that's what TFF requires.

We attempted to reverse engineer the deep learning image.

We did this by running

```
gcrane config gcr.io/deeplearning-platform-release/base-cpu:latest > ~/tmp/config.json
```

The resulting config has most of the commands in the Dockerfile. We used that
to construct Dockerfile. 

One modification is that we moved a lot of the multi-file commands into packages/setup.sh.

Most of the files in this directory were obtained by spinning up an instance of gcr.io/deeplearning-platform-release/base-cpu:latest
and then copying them.
