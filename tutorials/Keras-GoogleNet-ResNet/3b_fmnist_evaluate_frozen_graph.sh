#!/bin/bash

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



echo " "
echo "##########################################################################"
echo "EVALUATE FROZEN GRAPH of LeNet on Fashion MNIST"
echo "##########################################################################"
python code/eval_graph.py --graph ./freeze/fmnist/LeNet/frozen_graph.pb --input_node conv2d_1_input --output_node activation_4/Softmax  --gpu 0  2>&1 | tee rpt/fmnist/3b_evaluate_frozen_graph_LeNet.log

echo " "
echo "##########################################################################"
echo "EVALUATE FROZEN GRAPH of miniVggNet  on Fashion MNIST"
echo "##########################################################################"
python code/eval_graph.py --graph ./freeze/fmnist/miniVggNet/frozen_graph.pb --input_node conv2d_1_input --output_node activation_6/Softmax  --gpu 0  2>&1 | tee rpt/fmnist/3b_evaluate_frozen_graph_miniVggNet.log


echo " "
echo "##########################################################################"
echo "EVALUATE FROZEN GRAPH of GoogleNet  on Fashion MNIST"
echo "##########################################################################"
python code/eval_graph.py --graph ./freeze/fmnist/miniGoogleNet/frozen_graph.pb --input_node conv2d_1_input --output_node activation_20/Softmax  --gpu 0  2>&1 | tee rpt/fmnist/3b_evaluate_frozen_graph_miniGoogleNet.log

echo " "
echo "##########################################################################"
echo "EVALUATE FROZEN GRAPH of ResNet  on Fashion MNIST"
echo "##########################################################################"
python code/eval_graph.py --graph ./freeze/fmnist/miniResNet/frozen_graph.pb --input_node conv2d_1_input --output_node activation_83/Softmax  --gpu 0  2>&1 | tee rpt/fmnist/3b_evaluate_frozen_graph_miniResNet.log

echo " "
echo "##########################################################################"
echo "EVALUATE FROZEN GRAPH COMPLETED"
echo "##########################################################################"
echo " "
