# iceParsingPipeline

Pipelines to parse plain text files using either the Berkeley neural parser or the Berkeley parser. Both models are trained on IcePaHC.

The two pipelines and the Berkeley neural parser are licensed under the MIT license while the Berkeley parser is licensed under GPLv2.

### Using the neural pipeline

Download the parsing model from [Dropbox](https://www.dropbox.com/s/adblf1hh9ckxdg0/_dev%3D83.54.pt?dl=0) and save under the [/tools/neuralParser/](https://github.com/antonkarl/iceParsingPipeline/tree/master/tools/neuralParser) directory. Make sure not to change the name of the model. Run the command:

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

