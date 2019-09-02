# Pipeline to parse plain text files using the Berkeley parser
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
#


inputFile=$1
txtOutputFile=$2
outputFile=$3
tempfile='temp/temp.txt'
temppsd='temp/temp.psd'

# Command to run CorpusSearch (used for formatting trees)
CS="java -classpath ./tools/cs/CS_2.002.75.jar csearch/CorpusSearch"

# STEP 1: Use Kyle Gorman's Detector Morse for punctuation splitting.
echo 'Splitting sentences based on punctuation.'
python3 -m detectormorse -r ./tools/splitter/icepunct.gz -s $1 > $tempfile

# STEP 2: Matrix clause splitter developed by Anton Karl Ingason
# based on Kyle Gorman's design of Detector Morse)

echo 'Splitting matrix clauses.'
python3 ./tools/splitter/splitter.py ./tools/splitter/iceconj.gz $tempfile > $tempfile.out
mv -f $tempfile.out $tempfile

# STEP 3: Preprocessing for Parser (adjust whitespace)
echo 'Preparing input for Berkeley parser (adjusting whitespace)'
python3 ./tools/scripts/preprocess.py $tempfile $tempfile.out
mv -f $tempfile.out $tempfile
# Save txt output file (fully tokenized but not parsed)
mv $tempfile $txtOutputFile

# STEP 4: Run Berkeley Parser
echo 'Running Berkeley Parser (this may take a while)'
java -jar ./tools/parser/BerkeleyParser-1.7.jar -gr ./tools/parser/icegrammar.grammar -inputFile $txtOutputFile -outputFile $temppsd

# STEP 5: Restore dashes in phrase labels and tags
python3 ./tools/scripts/postprocess.py $temppsd $temppsd.dashed
mv -f $temppsd.dashed $temppsd

# STEP 6: Make output pretty
# This runs a structure changing CorpusSearch query that does
# nothing but reformat the output.
echo 'Formatting output'
./tools/cs/formatpsd.sh $temppsd $temppsd.pretty
mv -f $temppsd.pretty $temppsd

# STEP 7:  Saving output file
echo 'Saving output file'
mv -f $temppsd $outputFile

# Done
echo 'Done!'

