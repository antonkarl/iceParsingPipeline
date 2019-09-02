CS="java -classpath ./tools/cs/CS_2.002.75.jar csearch/CorpusSearch"

tempfile="temp.psd"
cp -f $1 $tempfile

$CS tools/cs/donothing.q $tempfile
mv -f $tempfile.out $tempfile

mv -f $tempfile $2
