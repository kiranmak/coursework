import string
import submission, util
from collections import defaultdict
from typing import List, Dict, Tuple
from submission import extractCharacterFeatures, extractWordFeatures, learnPredictor, testValuesOfN
import random

def mytestValuesOfN(n: int):
    '''
    Use this code to test different values of n for extractCharacterFeatures
    This code is exclusively for testing.
    Your full written solution for this problem must be in sentiment.pdf.
    '''
    featureExtractor = extractCharacterFeatures(n)
    #featureExtractor = lambda x:x
    weights = learnPredictor(trainExamples,
                             validationExamples,
                             featureExtractor,
                             numEpochs=20,
                             eta=0.01)
    util.outputWeights(weights, 'weights')
    util.outputErrorAnalysis(validationExamples, featureExtractor, weights,
                        'error-analysis')  # Use this to debug
    trainError = util.evaluatePredictor(
        trainExamples, lambda x:
        (1 if util.dotProduct(featureExtractor(x), weights) >= 0 else -1))
    validationError = util.evaluatePredictor(
        validationExamples, lambda x:
        (1 if util.dotProduct(featureExtractor(x), weights) >= 0 else -1))
    print((n, "- Official: train error = %s, validation error = %s" %
           (trainError, validationError)))
    
trainExamples = util.readExamples('polarity.train')
validationExamples = util.readExamples('polarity.dev')

'''
Write the generateExample function (nested in the generateDataset func-
tion) to generate artificial data samples.
Use this to double check that your learnPredictor works! You can do this by us-
ing generateDataset() to generate training and validation examples. You can then
pass in these examples as trainExamples and validationExamples respectively to
learnPredictor with the identity function lambda x:x as a featureExtractor.
'''

'''
weights = {}
for _ in range(100):
    k = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    v = random.uniform(-1, 1)
    weights[k] = v
temp = submission.generateDataset(50, weights)
trainExamples = temp[1:20]
validationExamples = temp[20:50]
#print(trainExamples)
'''

for n in range(2, 15):
    mytestValuesOfN(n)