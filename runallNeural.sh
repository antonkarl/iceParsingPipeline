# Pipeline to parse plain text files using the Berkeley neural parser
# and a model trained on IcePaHC.
# Usage: ./runall.sh inputfile.txt textOutputfile.txt outputfile.psd
#
# file1: plain text input
# file2: plain text output, split into matrix clauses
# file3: parsed .psd file formatted like IcePaHC
#
# Dependencies:
# python3
# -- package detectormorse (pip3 install detectormorse)
# java
# -- package tokenizer (pip3 install tokenizer)
# Cython (pip3 install cython)
# numpy (pip3 install numpy)
#


inputFile=$1
txtOutputFile=$2
outputFile=$3
tempfile=${inputFile%.txt}.temp
temppsd=${tempfile%.txt}.psd

# Command to run CorpusSearch (used for formatting trees)
CS="java -classpath ./tools/cs/CS_2.002.75.jar csearch/CorpusSearch"

# STEP 1: Use Greynir's tokenizer for punctuation splitting.
echo 'Splitting sentences based on punctuation.'
tokenize $1 > $tempfile

# STEP 2: Matrix clause splitter developed by Anton Karl Ingason
# based on Kyle Gorman's design of Detector Morse)
echo 'Splitting matrix clauses.'
python3 ./tools/splitter/splitter.py ./tools/splitter/iceconj.gz $tempfile > $tempfile.out
mv -f $tempfile.out $tempfile
# Save txt output file (fully tokenized but not parsed)
mv $tempfile $txtOutputFile

# STEP 3: Run Berkeley Neural Parser
echo 'Running Berkeley Neural Parser (this may take a while)'
python3 ./tools/neuralParser/src/main.py parse --model-path-base ./tools/neuralParser/_dev=84.91.pt --input-path $txtOutputFile --output-path $temppsd

# STEP 4: Restore dashes in phrase labels and tags and remove extra labels
python3 ./tools/scripts/postprocess.py $temppsd $temppsd.dashed
./tools/scripts/postprocessNeural.sh $temppsd.dashed
mv -f $temppsd.dashed $temppsd

# STEP 5: Make output pretty
# This runs a structure changing CorpusSearch query that does
# nothing but reformat the output.
echo 'Formatting output'
./tools/cs/formatpsd.sh $temppsd $temppsd.pretty
mv -f $temppsd.pretty $temppsd

# STEP 6:  Saving output file
echo 'Saving output file'
mv -f $temppsd $outputFile

# Done
echo 'Done!'
