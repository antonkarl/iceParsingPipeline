# Removes extra labels and brackets in parsed output

gsed -i 's/^(TOP //g' $1
gsed -i 's/)$//g' $1