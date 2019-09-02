import sys

inputFile = sys.argv[1]
outputFile = sys.argv[2]

with open(inputFile) as f:
    text = f.read()

text = text.replace('*','-')

with open(outputFile, 'w') as f:
    f.write(text)
