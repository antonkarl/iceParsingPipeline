# Removes extra labels in parsed output

sed -i 's/^(TOP\s/(/g' $1

# The GNU sed equivalent
#sed -i 's/^(TOP\s/(/g' $1
