import deeplake
ds = deeplake.load('hub://activeloop/fer2013-train')

import tensorflow as tf     
mnist = tf.keras.datasets.mnist     #

import pytorch as pytorch



dataloader = ds.pytorch(num_workers=0, batch_size=4, shuffle=False)

dataloader = ds.tensorflow()