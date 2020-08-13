#!/bin/bash

echo "Installing detectormorse..."
pip3 install detectormorse

echo "Installing Greynir's Tokenizer..."
pip3 install tokenizer

echo "Installing Cython..."
pip3 install cython

echo "Installing Numpy..."
pip3 install numpy

echo "Installing PyTorch..."
pip3 install torch==1.1.0 torchvision==0.3.0

echo "Installing a pretrained BERT model..."
pip3 install pytorch-pretrained-bert

echo "Installation finished!"