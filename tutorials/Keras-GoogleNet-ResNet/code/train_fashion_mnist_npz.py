#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
## © Copyright (C) 2016-2020 Xilinx, Inc
##
## Licensed under the Apache License, Version 2.0 (the "License"). You may
## not use this file except in compliance with the License. A copy of the
## License is located at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
## WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
## License for the specific language governing permissions and limitations
## under the License.
'''

# USAGE
# python train_fashion_mnist.py --network LeNet      --weights keras_model/fmnist/LeNet      --epochs   5 --init_lr 0.01 --batch_size 32
# python train_fashion_mnist.py --network miniVggNet --weights keras_model/fmnist/miniVggNet --epochs  25 --init_lr 0.01 --batch_size 64
# python train_fashion_mnist.py --network miniResNet --weights keras_model/fmnist/miniResNet --epochs 100 --init_lr 0.1  --batch_size 128


# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

from config import fashion_mnist_config as cfg #DB
from custom_cnn import ConvNetFactory

# import the necessary packages
from sklearn.metrics import classification_report
from keras.optimizers import SGD
from keras import backend as K
#import tensorflow.keras as K
#from imutils import build_montages
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime #DB
from keras.utils import plot_model #DB
from keras.callbacks import ModelCheckpoint #DB
from keras.callbacks import LearningRateScheduler
import os # DB

from keras.preprocessing.image import ImageDataGenerator

##################################################################################

import argparse #DB
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-w",  "--weights", default="keras_model/fmnist/LeNet", help="path to best model HDF5 weights file")
ap.add_argument("-n",  "--network", default="LeNet",             help="input CNN")
ap.add_argument("-d",  "--dropout", type=int, default=-1,    help="whether or not Dropout should be used")
ap.add_argument("-bn", "--BN",      type=int, default=-1,    help="whether or not BN should be used")
ap.add_argument("-e",  "--epochs", type=int, default=5,     help="# of epochs")
ap.add_argument("-bs", "--batch_size", type=int, default=32, help="size of mini-batches passed to network")
ap.add_argument("-l",  "--init_lr", type=float, default=0.01,  help="initial Learning Rate")
args = vars(ap.parse_args())

weights = args["weights"]
network = args["network"]
##################################################################################
# initialize the number of epochs to train for, base learning rate,
# and batch size
NUM_EPOCHS = args["epochs"]     #25
INIT_LR    = args["init_lr"]    #1e-2
BATCH_SIZE = args["batch_size"] #32

#################################################################################
# create data from images

data=np.load('fmnist_dataset.npz')
x_train = data['x_train']
y_train = data['y_train']
x_test = data['x_test']
y_test = data['y_test']
x_valid = data['x_valid']
y_valid = data['y_valid']

##################################################################################################
# construct the callback to save only the *best* model to disk
# based on the validation loss
fname = os.path.sep.join([weights, "best_chkpt.hdf5"])
checkpoint = ModelCheckpoint(fname,
		monitor="val_loss", mode="min",
		#monitor="val_acc", mode="max",
		save_best_only=True, verbose=1)

callbacks_list = [checkpoint]



def poly_decay(epoch):
                # initialize the maximum number of epochs, base learning rate, and power of the polynomial
                maxEpochs = NUM_EPOCHS
                baseLR = INIT_LR
                power = 1.0
                # compute the new learning rate based on polynomial decay
                alpha = baseLR * (1 - (epoch / float(maxEpochs))) ** power
                # return the new learning rate
                return alpha

if network == "miniResNet" :
                callbacks_list = [checkpoint, LearningRateScheduler(poly_decay)]


##################################################################################################
# initialize the optimizer and model
print("[INFO] compiling model...")

if network == "miniResNet" :
        model = ConvNetFactory.build(network, width=cfg.IMAGE_WIDTH, height=cfg.IMAGE_HEIGHT,
                                     depth=3, classes=cfg.NUM_CLASSES,
                                     stages=(9, 9, 9),
                                     filters=(64, 64, 128, 256),
                                     reg=0.0005)
        opt = SGD(lr=INIT_LR, momentum=0.9)
else:
        model = ConvNetFactory.build(network, width=cfg.IMAGE_WIDTH, height=cfg.IMAGE_HEIGHT, depth=3, classes=cfg.NUM_CLASSES, FC=True) #FC=False)
        opt = SGD(lr=INIT_LR, momentum=0.9, decay=INIT_LR / NUM_EPOCHS)

model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])


##################################################################################################
# data genarators
test_datagen =ImageDataGenerator()
train_datagen =ImageDataGenerator()
valid_datagen=ImageDataGenerator()
aug_datagen = ImageDataGenerator(
        #rescale=1/255,
        rotation_range=5,
        horizontal_flip=True,
        height_shift_range=0.1,
        width_shift_range=0.1,
        shear_range=0.2,
        zoom_range=0.2)

aug_generator = aug_datagen.flow(
        x_train, y_train,
        batch_size=BATCH_SIZE)

train_generator = train_datagen.flow(
        x_train, y_train,
        batch_size=BATCH_SIZE)

validation_generator = valid_datagen.flow(
        x_valid, y_valid,
        batch_size=BATCH_SIZE)

pred_generator = test_datagen.flow(
        x_test, y_test,
        batch_size=1)

##################################################################################################
# train the network
print("[INFO] training model...")
startTime1 = datetime.now() #DB
# run training

if network == "miniResNet" :
        H = model.fit_generator(aug_generator,
                                steps_per_epoch=len(x_train)//NUM_EPOCHS, epochs=NUM_EPOCHS,
                                validation_data=validation_generator,
                                validation_steps=len(x_valid)//NUM_EPOCHS,
                                callbacks=callbacks_list,
                                shuffle=True,verbose=2)
else:
        H = model.fit_generator(train_generator,
                                steps_per_epoch=len(x_train)//NUM_EPOCHS,epochs=NUM_EPOCHS,
                                validation_data=validation_generator,
                                validation_steps=len(x_valid)//NUM_EPOCHS,
                                callbacks=callbacks_list,
                                shuffle=True,verbose=2)

endTime1 = datetime.now()
diff1 = endTime1 - startTime1
print("\n")
print("Elapsed time for Keras training (s): ", diff1.total_seconds())
print("\n")


##################################################################################################
print("[INFO] evaluating network on Test and Validation datasets...")
# Evaluate model accuracy with test set
scores = model.evaluate(x_valid, y_valid, batch_size=BATCH_SIZE) #MH
print('Validation Loss: %.3f'     % scores[0]) #MH
print('validation Accuracy: %.3f' % scores[1]) #MH
scores = model.evaluate(x_test, y_test, batch_size=BATCH_SIZE) #MH
print('Test Loss: %.3f'     % scores[0]) #MH
print('Test Accuracy: %.3f' % scores[1]) #MH

# make predictions on the test set
preds = model.predict(x_test)
# show a nicely formatted classification report
print(classification_report(y_test.argmax(axis=1), preds.argmax(axis=1), target_names=cfg.labelNames_list))

# plot the training loss and accuracy
N = NUM_EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy on Dataset")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig("./doc/images/" + network + "_plot.png")


##################################################################################################
# plot the CNN model #DB
plot_model(model, to_file="./doc/images/bd_"+network+".png", show_shapes=True)


##################################################################################################
# save CNN complete model on HDF5 file #DB
fname1 = os.path.sep.join([weights, "final.hdf5"])
model.save(fname1)

# once saved the model can be load with following commands #DB
#from keras.models import load_model #DB
#print("[INFO] loading pre-trained network...") #DB
#model = load_model(fname) #DB


##################################################################################################
print("\nTRAINING " + network + " FINISHED\n")
