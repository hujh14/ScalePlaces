import os
import argparse
import numpy as np
from scipy import misc
import h5py

import utils_eval as utils

def evaluate_image(im, threshold=0):
    cm = utils.get(im, CONFIG, ftype="cm")
    ap = utils.get(im, CONFIG, ftype="ap")
    gt = utils.get(im, CONFIG, ftype="gt")

    accuracy = {}
    for i in xrange(150):
        c = i+1
        probs = ap[:,:,i]
        prob_mask = prob[prob > threshold]
        print prob_mask.dtype
        print prob_mask.shape
        
        cm_mask = cm == c
        gt_mask = gt == c
        intersection = np.logical_and(cm_mask, gt_mask)
        union = np.logical_or(cm_mask, gt_mask)

        if np.sum(union) != 0:
            iou = 1.0*np.sum(intersection)/np.sum(union)
            gt_area = np.sum(gt_mask)
            accuracy[c] = iou
    return accuracy

def evaluate_images(im_list):
    n = len(im_list)
    accuracies = np.zeros((n, 150))
    for i in xrange(n):
        im = im_list[i]
        print im

        try:
            accuracy = evaluate_image(im)
        except:
            accuracy = {}
            print "Skipping", im

        for c in xrange(1,151):
            if c in accuracy:
                accuracies[i,c-1] = accuracy[c]
            else:
                accuracies[i,c-1] = np.nan
    return accuracies

parser = argparse.ArgumentParser()
parser.add_argument("-p", required=True, help="Project name")
args = parser.parse_args()

project = args.p
CONFIG = utils.get_data_config(project)

im_list = [line.rstrip() for line in open(config["im_list"], 'r')]
im_list = im_list[:100]
accuracies = evaluate_images(im_list)
print accuracies.shape

fname = "{}_acc_squish.h5".format(project)
with h5py.File(fname, 'w') as f:
    f.create_dataset('accuracies', data=accuracies)
