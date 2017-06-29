import os
import random

import utils_vis as utils
from vis import Visualizer

output_dir = "vis_places"
project = "places"
config = utils.get_data_config(project)

vis = Visualizer(project, output_dir, MAX=100)
for i in xrange(0):
    im_list = [line.rstrip() for line in open(config["im_list"], 'r')]
    random.shuffle(im_list)
    vis.makeHTML(im_list,fname="{}_{}.html".format(project, i))

im_list_dir = "../eval/sorted/{}".format(project)
for fname in os.listdir(im_list_dir):
    if ".txt" not in fname:
        continue
    im_list = [line for line in open(os.path.join(im_list_dir,fname), 'r')]
    vis.makeHTML(im_list, fname=fname.replace(".txt", ".html"))
