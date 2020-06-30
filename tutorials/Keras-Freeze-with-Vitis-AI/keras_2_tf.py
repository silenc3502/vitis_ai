'''
 Copyright 2020 Xilinx Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
'''


'''
 load Keras saved model in JSON and/or HDF5 format and create TensorFlow checkpoint and 
 inference graph.

 Usage:

   If Keras model is contained in a JSON file and HDF5 file, then the paths to these files
   should be provided using the --keras_json and --keras_hdf5 arguments.

   If no --keras_json argument is provided, then the script assumes that the network architecture 
   and weights are all contained in the HDF5 file provided by the --keras_hdf5 arguments.

   The TensorFlow graph will be created in either binary or text format according to the filename 
   provided in the --tf_graph argument.  A text format graph will be created for a .pbtxt filename extension 
   and a binary format graph will be created for any other filename extension.

   If the --tf_graph and --tfckpt arguments contain paths with folder names that do not exist, then the 
   folders will be created. If the files already exist, they will be overwritten.
'''

import os
import argparse
import sys

import keras
from keras import backend
from keras.models import model_from_json, load_model
import tensorflow as tf

# Silence TensorFlow messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


def keras2tf(keras_json,keras_hdf5,tfckpt):
        
    # set learning phase for no training
    backend.set_learning_phase(0)

    # if name of JSON file provided as command line argument, load from 
    # arg.keras_json and args.keras_hdf5.
    # if JSON not provided, assume complete model is in HDF5 format
    if (keras_json != ''):
        json_file = open(keras_json, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(keras_hdf5)

    else:
        loaded_model = load_model(keras_hdf5)


    print ('Keras model information:')
    print (' Input names :',loaded_model.inputs)
    print (' Output names:',loaded_model.outputs)
    print('-------------------------------------')

    # set up tensorflow saver object
    saver = tf.train.Saver()

    # fetch the tensorflow session using the Keras backend
    tf_session = backend.get_session()

    # get the tensorflow session graph
    input_graph_def = tf_session.graph.as_graph_def()

    # write out tensorflow checkpoint & inference graph for use with freeze_graph script
    save_path = saver.save(tf_session, tfckpt)

    print ('TensorFlow information:')
    print (' Checkpoint saved as:',tfckpt)
    print('-------------------------------------')

    return



# only used if script is run as 'main' from command lime
def main():
  # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument('-kj', '--keras_json',
                    type=str,
                    default='',
    	            help='path of Keras JSON. Default is empty string to indicate no JSON file')    
    ap.add_argument('-kh', '--keras_hdf5',
                    type=str,
                    default='./model.hdf5',
    	            help='path of Keras HDF5. Default is ./model.hdf5')
    ap.add_argument('-tfc', '--tfckpt',
                    type=str,
                    default='./tfchkpt.ckpt',
    	            help='path of TensorFlow checkpoint. Default is ./tfchkpt.ckpt')
    args = ap.parse_args()


    print('\n------------------------------------')
    print('Keras version      :',keras.__version__)
    print('TensorFlow version :',tf.__version__)
    print('Python version     :',(sys.version))
    print('-------------------------------------')
    print('keras_2_tf command line arguments:')
    print(' --keras_json:', args.keras_json)
    print(' --keras_hdf5:', args.keras_hdf5)
    print(' --tfckpt    :', args.tfckpt)
    print('-------------------------------------')

    keras2tf(args.keras_json,args.keras_hdf5,args.tfckpt)



if __name__ == '__main__':
  main()


