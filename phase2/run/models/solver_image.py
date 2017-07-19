net: "models/train_image.prototxt"
display: 40
average_loss: 20 # Display loss averaged over last x iterations
snapshot: 1000
snapshot_prefix: "snapshots/image/snapshot"

base_lr: 1e-11
lr_policy: "fixed"
momentum: 0.5
weight_decay: 0.0005
iter_size: 1 # no gradient accumulation between iterations
max_iter: 300000

# Make a separate test net
test_initialization: false
test_iter: 10
test_interval: 999999999
