import os
import sys
import time
import random
import socket
import numpy as np

import utils_run as utils
import pspnet_utils

CAFFE_ROOT = '/data/vision/torralba/segmentation/places/PSPNet/'
sys.path.insert(0, os.path.join(CAFFE_ROOT, 'python'))
import caffe

WEIGHTS = '/data/vision/torralba/segmentation/places/PSPNet/evaluation/model/pspnet50_ADE20K.caffemodel'

class PSPNet:
    def __init__(self, DEVICE=0):
        caffe.set_mode_gpu()
        caffe.set_device(DEVICE)

        SEED = 3
        random.seed(SEED)

        # MODEL_INFERENCE = 'models/train_pspnet_modified.prototxt'
        MODEL_INFERENCE = 'models/pspnet50_ADE20K_473.prototxt'

        self.net = caffe.Net(MODEL_INFERENCE, WEIGHTS, caffe.TEST)

        self.log = 'logs/%s_seed%d_gpu%d.log'%(socket.gethostname(), SEED, DEVICE)

    def fine_tune(self):
        solver = caffe.get_solver('models/solver_pspnet_modified.prototxt')
        solver.net.copy_from(WEIGHTS)

    def process(self, image):
        if image.ndim != 3:
            image = np.stack((image,image,image), axis=2)
        h_ori,w_ori,_ = image.shape

        image_scaled = pspnet_utils.scale(image)
        crops = pspnet_utils.split_crops(image_scaled)

        crop_probs = []
        for crop in crops:
            crop_prob = self.feed_forward(crop)
            crop_probs.append(crop_prob)

        probs = pspnet_utils.assemble_probs(image_scaled,crop_probs)
        probs = pspnet_utils.unscale(probs,h_ori,w_ori)

        return probs
        

    def feed_forward(self, data):
        '''
        Input must be 473x473x3 in RGB
        Output is 150x473x473
        '''
        assert data.shape == (473,473,3)
        # RGB => BGR
        data = data[:,:,(2,1,0)]
        data = data.transpose((2,0,1))
        data = data[np.newaxis,:,:,:]

        self.net.blobs['data'].data[...] = data
        self.net.forward()
        out = self.net.blobs['prob'].data[0,:,:,:]
        return out
        

    def get_network_architecture(self):
        for k,v in self.net.blobs.items():
            print v.data.shape, k








