#!/bin/bash

# Copyright 2019 Xilinx Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



# evaluate graph
run_eval_graph() {
  graph=$1
  python eval_graph.py \
    --graph=$graph \
    --input_node=${INPUT_NODE} \
    --output_node=${OUTPUT_NODE} \
    --batchsize=100 \
    --gpu=0
}



eval() {

  echo "-----------------------------------------"
  echo " EVALUATING THE FROZEN GRAPH.."
  echo "-----------------------------------------"

  # evaluate the frozen graph performance
  run_eval_graph ${FREEZE}/${FROZEN_GRAPH} 2>&1 | tee ${LOG}/${EVAL_FR_LOG}


  echo "-----------------------------------------"
  echo "GRAPH EVAL COMPLETED"
  echo "-----------------------------------------"
}

eval
