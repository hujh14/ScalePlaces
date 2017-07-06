import numpy as np
import itertools
from scipy import misc, ndimage

DATA_MEAN = np.array([[[123.68, 116.779, 103.939]]])
INPUT_SIZE = 473
NUM_CLASS = 150

stride_rate = 0.3
scale_size = 512

def split_crops(image):
    h,w,_ = image.shape
    crop_boxes = get_crop_boxes(h,w)
    n = len(crop_boxes)

    crops = np.zeros((n,INPUT_SIZE,INPUT_SIZE))
    for i in xrange(n):
        sh,eh,sw,ew = crop_boxes[i]

        crop = np.tile(DATA_MEAN, (INPUT_SIZE, INPUT_SIZE, 1))
        crop[0:eh-sh,0:ew-sw,:] = image[sh:eh,sw:ew,:]
        crops[i] = crop
    return crops

def assemble_probs(image, probs):
    h,w,_ = image.shape
    probs = np.zeros((NUM_CLASS, h, w), dtype=np.float32)
    cnts = np.zeros((1,h,w))

    crop_boxes = get_crop_boxes(h,w)
    n = len(crop_boxes)
    for i in xrange(n):
        sh,eh,sw,ew = crop_boxes[i]
        prob = probs[i]

        probs[:,sh:eh,sw:ew] += prob[:,0:eh-sh,0:ew-sw]
        cnts[0,sh:eh,sw:ew] += 1

    assert cnts.min()>=1
    probs /= cnts
    assert (probs.min()>=0 and probs.max()<=1), '%f,%f'%(probs.min(),probs.max())
    return probs

def scale(image):
    h = image.shape[0]
    w = image.shape[1]
    short_side = min(h, w)
    long_side = max(h, w)
    ratio = 1.*scale_size/long_side # Make long_side == scale_size
    return misc.imresize(image, ratio)

def unscale(probs,h_ori,w_ori):
    _,h,w = probs.shape
    probs_scaled = ndimage.zoom(probs, (1.,1.*h_ori/h,1.*w_ori/w), order=1, prefilter=False, mode='nearest')
    return probs_scaled

def get_crop_boxes(h,w):
    boxes = []
    crop_locs = get_crop_locs(h,w)
    for loc in crop_locs:
        sh,sw = loc
        eh = min(h, sh + INPUT_SIZE)
        ew = min(w, sw + INPUT_SIZE)
        box = (sh,eh,sw,eh)
        boxes.append(box)
    return boxes

def get_crop_locs(h,w):
    stride = INPUT_SIZE * stride_rate
    hs_upper = max(1,h-(INPUT_SIZE-stride))
    ws_upper = max(1,w-(INPUT_SIZE-stride))
    hs = np.arange(0,hs_upper,stride, dtype=int)
    ws = np.arange(0,ws_upper,stride, dtype=int)
    locs = list(itertools.product(hs,ws))
    return locs