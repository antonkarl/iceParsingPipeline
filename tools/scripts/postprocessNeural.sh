# Removes extra labels and brackets in parsed output

sed -i 's/^(TOP\s//g' $1
sed -i 's/)$//g' $1
