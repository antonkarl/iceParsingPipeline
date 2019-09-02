import logging
import sys
import re
from collections import namedtuple
from re import finditer, match, search
from detectormorse.ptbtokenizer import word_tokenize

from nlup import listify, BinaryAveragedPerceptron, BinaryConfusion, JSONable

# defaults
EPOCHS = 20     # number of epochs (iterations for classifier training)
BUFSIZE = 32    # for reading in left and right contexts...see below

# regexes

TARGET = r"(\s+)(og|eða|en)(\s+)"

# LTOKEN = r"(\S+)\s*$"
LTOKEN = r"(\S+)\s*(\S+)\s*$"

#RTOKEN = r"^\s*(\S+)"
RTOKEN = r"^\s*(\S+)\s*(\S+)"


NEWLINE = r"^\s*[\r\n]+\s*$"

# other

Observation = namedtuple("Observation", ["left","conjunction","right","boundary","end"])


class IceTags():

    def __init__(self):
        self.wordtags = self.load_wordtags()

    def is_finite(self, word):
        if not word.lower() in self.wordtags:
            return False
        
        for tag in self.wordtags[word.lower()]:
            if match(r"(VB|HV|DO|RD|MD|BE)[PD][IS]",tag):
                return True
        return False

    def is_nonfinite(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if match(r"(VB|HV|DO|RD|MD|BE|VA|DA|RA)[N]?",tag):
                return True
        return False
            
    def is_nominative(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if match("(\S+)\-N", tag):
                return True
        return False

    def is_oblique(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if match("(\S+)\-[ADG]", tag):
                return True
        return False


    def load_wordtags(self):
        with open('wordtags.tsv') as f:
            wordtags = dict()
            lines = f.read().splitlines()
            for line in lines:
                key, values = line.split('\t')
                wordtags[key] = values.split()

        return wordtags

def slurp(filename, encoding='utf-8'):
    """
    Given a `filename` string, slurp the whole file into a string
    """
    with open(filename, encoding=encoding) as source:
        return source.read()
    

class TreeSplitter(JSONable):

    def __init__(self, text=None, epochs=EPOCHS,
                 classifier=BinaryAveragedPerceptron, **kwargs):
        self.classifier = classifier(**kwargs)
        self.icetags = IceTags()

        if text:

            text = text.replace(',', ' ,')
            text = text.replace(':', ' :')
            text = text.replace('.', ' .')
            self.fit(text, epochs)

    def __repr__(self):
        return "{}(classifier={!r})".format(self.__class__.__name__,
                                            self.classifier)

    @staticmethod
    def candidates(text):
        """
        Given a `text` string, get candidates and context for feature
        extraction and classification
        """

        for Cmatch in finditer(TARGET, text):
            # the conjunction itself
            conjunction = Cmatch.group(2)
            boundary = bool(match(NEWLINE,Cmatch.group(1)))

            # L & R
            start = Cmatch.start()
            end = Cmatch.end()
            Lmatch = search(LTOKEN, text[max(0, start - BUFSIZE):start])
            if not Lmatch:  # this happens when a line begins with '.'
                continue
            left = word_tokenize(Lmatch.group())
            # left = Lmatch.group()

            Rmatch = search(RTOKEN, text[end:end + BUFSIZE])
            if not Rmatch:  # this happens at the end of the file, usually
                continue

            #right = word_tokenize(Rmatch.group(1) + " ")[0]    
            right = word_tokenize(Rmatch.group())    

            # complete observation
            yield Observation(left, conjunction, right, boundary, end)     


    @listify
    def extract_one(self, left, conjunction, right):
        """
        Given left context, conjunction, and right context, 
        extract features. Probability distributions for any
        quantile-based features will not be modified.
        """
        yield "*bias*"

        if left[1] == ',':
            yield 'L1comma'


        # finiteness
        if self.icetags.is_finite(left[0]):
            yield 'L0finite'
        if self.icetags.is_finite(left[1]):
            yield 'L1finite'
        if self.icetags.is_finite(right[0]):
            yield 'R0finite'
        if self.icetags.is_finite(right[1]):
            yield 'R1finite'


        # non-finiteness
        if self.icetags.is_nonfinite(left[0]):
            yield 'L0nonfinite'
        if self.icetags.is_nonfinite(left[1]):
            yield 'L1nonfinite'
        if self.icetags.is_nonfinite(right[0]):
            yield 'R0nonfinite'
        if self.icetags.is_nonfinite(right[1]):
            yield 'R1nonfinite'


        # nominative
        if self.icetags.is_nominative(left[0]):
            yield 'L0nom'
        if self.icetags.is_nominative(left[1]):
            yield 'L1nom'
        if self.icetags.is_nominative(right[0]):
            yield 'R0nom'
        if self.icetags.is_nominative(right[1]):
            yield 'R1nom'

        # oblique
        if self.icetags.is_oblique(left[0]):
            yield 'L0obl'
        if self.icetags.is_oblique(left[1]):
            yield 'L1obl'
        if self.icetags.is_oblique(right[0]):
            yield 'R0obl'
        if self.icetags.is_oblique(right[1]):
            yield 'R1obl'
            

    def fit(self, text, epochs=EPOCHS):
        """
        Given a string `text`, use it to train the segmentation classifier
        for `epochs` iterations.
        """
        logging.debug("Extracting features and classifications.")
        Phi = []
        Y = []
        for (left, conjunction, right, gold, _) in self.candidates(text):
            Phi.append(self.extract_one(left, conjunction, right))
            Y.append(gold)
        self.classifier.fit(Y, Phi, epochs)
        logging.debug("Fitting complete.")
    

    def predict(self, left, conjunction, right):
        """
        Given an left context `L`, punctuation mark `P`, and right context
        `R`, return True iff this observation is hypothesized to be a
        sentence boundary.
        """
        phi = self.extract_one(left, conjunction, right)
        return self.classifier.predict(phi)


    def segments(self, text, strip=True):
        """
        Given a string of `text`, return a generator yielding each
        hypothesized sentence string
        """
        start = 0
        for (L, conjunction, R, B, end) in self.candidates(text):
            if self.predict(L, conjunction, R):
                sent = text[start:end-len(conjunction)-2]
                if strip:
                    sent = sent.rstrip()
                yield sent
                start = end-len(conjunction)-1
            # otherwise, there's probably not a sentence boundary here
        sent = text[start:]
        if strip:
            sent = sent.rstrip()
        yield sent

    def evaluate(self, text):
        """
        Given a string of `text`, compute confusion matrix for the
        classification task.
        """
        cx = BinaryConfusion()
        for (L, P, R, gold, _) in self.candidates(text):
            guess = self.predict(L, P, R)
            cx.update(gold, guess)
            if not gold and guess:
                logging.debug("False pos.: L='{}', R='{}'.".format(L, R))
            elif gold and not guess:
                logging.debug("False neg.: L='{}', R='{}'.".format(L, R))
        return cx
        

#with open('sentences2.txt') as f:
#    text = f.read()[:20000]
#
#ts = TreeSplitter()

tsplitter = TreeSplitter.load(sys.argv[1])
output = "\n".join(tsplitter.segments(slurp(sys.argv[2])))
output = re.sub(r'\n+','\n',output).strip()
print(output)

