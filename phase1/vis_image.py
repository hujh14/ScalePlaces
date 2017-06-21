import argparse
import os
import uuid

from scipy import misc
import numpy as np

import utils

class ImageVisualizer:

    def __init__(self, project):
        self.images_dir = "tmp/images/"
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)

        config = utils.get_data_config(project)
        self.root_images = config["images"]
        self.root_cm = os.path.join(config["pspnet_prediction"], "category_mask")
        self.root_pm = os.path.join(config["pspnet_prediction"], "prob_mask")
        self.root_gt = config["ground_truth"]

    def visualize(self, im):

        im_path = os.path.join(self.root_images, im)
        cm, cm_path = self.get_category_mask(im)
        pm, pm_path = self.get_prob_mask(im)
        gt, gt_path = self.get_ground_truth(im)

        cm_color, cm_color_path = self.add_color(cm)
        gt_color, gt_color_path = self.add_color(gt)

        diff = self.get_diff(cm, gt)
        diff_color, diff_color_path = self.add_color(diff)

        paths = {}
        paths["image"] = im_path
        paths["category_mask"] = cm_color_path
        paths["prob_mask"] = pm_path
        paths["ground_truth"] = gt_color_path
        paths["diff"] = diff_color_path
        return paths

    def get_category_mask(self, im):
        try:
            path = os.path.join(self.root_cm, im.replace('.jpg','.png'))
            img = misc.imread(path)
            return img, path
        except:
            return None, None

    def get_prob_mask(self, im):
        try:
            path = os.path.join(self.root_pm, im)
            img = misc.imread(path)
            return img, path
        except:
            return None, None

    def get_ground_truth(self, im):
        try:
            path = os.path.join(self.root_gt, im.replace('.jpg','.png'))
            img = misc.imread(path)
            return img, path
        except:
            return None, None

    def get_diff(self, cm, gt):
        if cm is None or gt is None:
            return None
        mask = gt - cm
        mask = np.invert(mask.astype(bool))
        diff = np.copy(gt)
        diff[mask] = 0
        return diff

    def add_color(self, img):
        if img is None:
            return None, None

        h,w = img.shape
        img_color = np.zeros((h,w,3))
        for i in xrange(1,151):
            img_color[img == i] = utils.to_color(i)
        path = self.save(img_color)
        return img_color, path

    def save(self, img):
        fname = "{}.jpg".format(uuid.uuid4().hex)
        path = os.path.join(self.images_dir, fname)
        misc.imsave(path, img)
        return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", required=True, help="Project name")
    parser.add_argument("-i", help="Image name")
    args = parser.parse_args()

    project = args.p
    im = args.i
    if not im:
        f = utils.get_data_config(project)["im_list"]
        im_list = [line.rstrip() for line in open(f, 'r')]
        im = im_list[0]

    print project, im
    vis = ImageVisualizer(project)
    paths = vis.visualize(im)
    print paths

