import sys

inputFile = sys.argv[1]
outputFile = sys.argv[2]

with open(inputFile, encoding='utf-8') as f:
    text = f.read()

text = text.replace('*','-')

with open(outputFile, 'w', encoding='utf-8') as f:
    f.write(text)
