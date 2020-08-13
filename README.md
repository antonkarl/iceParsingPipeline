# iceParsingPipeline

Pipelines to parse plain text files using either the Berkeley neural parser or the Berkeley parser. Both models are trained on IcePaHC.

The two pipelines and the Berkeley neural parser are licensed under the MIT license while the Berkeley parser is licensed under GPLv2.

### Setting up the pipeline

The pipeline requires both Python 3.6>= and Java. Once both programs have been installed, the rest of the dependencies can be installed. Run ```./setup.sh``` to install all necessary dependencies. All dependencies are listed below.

### Using the neural pipeline

Download the parsing model from [here](https://notendur.hi.is/~antoni/ltdata/_dev=84.91.pt) (2.2 GB) and save under the [/tools/neuralParser/](https://github.com/antonkarl/iceParsingPipeline/tree/master/tools/neuralParser) directory. Make sure not to change the name of the model. Run the command:

```
$ ./runallNeural.sh inputfile.txt textOutputfile.txt outputfile.psd
```

file1: plain text input

file2: plain text output, split into matrix clauses

file3: parsed .psd file formatted like IcePaHC

### Using the previous pipeline

Run the command:

```
$ ./runall.sh inputfile.txt textOutputfile.txt outputfile.psd
```

file1: plain text input

file2: plain text output, split into matrix clauses

file3: parsed .psd file formatted like IcePaHC


# Dependencies

python3

-- package detectormorse (pip3 install detectormorse)

java

Additional dependencies needed for the neural parsing pipeline:

-- package tokenizer (pip3 install tokenizer)

Cython (pip3 install cython)

numpy (pip3 install numpy)

PyTorch version 0.4.1 or 1.0/1.1 (pip3 install torch==1.1.0 torchvision==0.3.0)

pytorch-pretrained-bert (pip3 install pytorch-pretrained-bert)

