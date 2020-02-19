# iceParsingPipeline

Pipelines to parse plain text files using either the Berkeley neural 
parser or the Berkeley parser. Both models are trained on IcePaHC.

Usage for the neural pipeline: ./runallNeural.sh inputfile.txt textOutputfile.txt outputfile.psd

Usage for the previous pipeline: ./runall.sh inputfile.txt textOutputfile.txt outputfile.psd

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

GNU sed (brew install gnu-sed) for macOS


