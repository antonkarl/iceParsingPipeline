import sys
import re

inputFile = sys.argv[1]
outputFile = sys.argv[2]

with open(inputFile, encoding='utf-8') as f:
    text = f.read()

# Let there be whitespace around punctuation symbols
text = text.replace(';',' ;')
text = text.replace(',',' ,')
text = text.replace('.',' .')
text = text.replace(':',' :')
text = text.replace('!',' !')
text = text.replace('?',' ?')
text = text.replace('\"',' \" ')

text = re.sub(' +',' ',text)

with open(outputFile, 'w', encoding='utf-8') as f:
    f.write(text)
    

    

