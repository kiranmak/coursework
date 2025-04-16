#!/usr/bin/python

import random
from typing import Callable, Dict, List, Tuple, TypeVar
from collections import defaultdict

from util import *

FeatureVector = Dict[str, int]
WeightVector = Dict[str, float]
Example = Tuple[FeatureVector, int]

############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction


def extractWordFeatures(x: str) -> FeatureVector:
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x:
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    fv = {}
    print(x)
    wlist = x.split(" ")
    for w in wlist:
        fv[w] = 1 if w not in fv else fv[w] + 1
    return fv
    # END_YOUR_CODE


############################################################
# Problem 3b: stochastic gradient descent

T = TypeVar('T')


class SPV:
    def dot(self, x, w):
        sump = 0
        for key in x.keys():
            sump += x[key] * w.get(key, 0)
        return sump

    def scalar_product(self, scale, v):
        product = {k: v[k] * scale for k in v.keys()}
        return product

    def sum(self, d1, d2):
        value = {k: d1.get(k, 0) + d2.get(k, 0) for k in d1.keys() | d2.keys()}
        return value

    def diff(self, d1, d2):
        value = {k: d1.get(k, 0) - d2.get(k, 0) for k in d1.keys() | d2.keys()}
        return value

def learnPredictor(trainExamples: List[Tuple[T, int]],
                   validationExamples: List[Tuple[T, int]],
                   featureExtractor: Callable[[T], FeatureVector],
                   numEpochs: int, eta: float) -> WeightVector:
    '''
    Given |trainExamples| and |validationExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of epochs to
    train |numEpochs|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Notes:
    - Only use the trainExamples for training!
    - You should call evaluatePredictor() on both trainExamples and
      validationExamples to see how you're doing as you learn after each epoch.
    - The predictor should output +1 if the score is precisely 0.
    '''
    # BEGIN_YOUR_CODE (our solution is 13 lines of code, but don't worry if you deviate from this)

    def predict(x):
        phi=featureExtractor(x)
        if dotProduct(weights,phi)<0.0:
            return -1
        else:
            return 1
        
    weights = {}  # feature => weight
    for t in range(numEpochs):
        for d_train in trainExamples:
            x, y = d_train
            phi = featureExtractor(x)
            dot_x_w = dotProduct(phi, weights) #w.phi 
            gradient = {}
            increment(gradient, 2*(dot_x_w - y), phi) #gradient = 2 *(w.phi(x) - y)phi(x)
            #SGD
            increment(weights, -eta, gradient) # w = w - eta * gradient
        #print(f"t:{t}, Train_error:", evaluatePredictor(trainExamples,predict), end="")
        #print(" validation_error:", evaluatePredictor(validationExamples,predict))

    # END_YOUR_CODE
    return weights


############################################################
# Problem 3c: generate test case


def generateDataset(numExamples: int, weights: WeightVector) -> List[Example]:
    '''
    Return a set of examples (phi(x), y) randomly which are classified
      correctly by |weights|.
    '''
    random.seed(42)

    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a score for the given weight vector.
    # note that there is intentionally flexibility in how you define phi.
    # y should be 1 or -1 as classified by the weight vector.
    # IMPORTANT: In the case that the score is 0, y should be set to 1.

    # Note that the weight vector can be arbitrary during testing.
    def generateExample() -> Tuple[Dict[str, int], int]:
        # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
        phi = {}
        for key in random.sample(list(weights),len(weights)):
            phi[key] = random.randint(-10, 10)
        y = 1 if dotProduct(phi, weights) >= 0 else -1
        # END_YOUR_CODE
        return phi, y

    return [generateExample() for _ in range(numExamples)]


############################################################
# Problem 3d: character features


def extractCharacterFeatures(n: int) -> Callable[[str], FeatureVector]:
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces mapped to their n-gram counts.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that 1 <= n <= len(x).
    '''
    def extract(x: str) -> Dict[str, int]:
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        out = {}
        x = x.replace(" ","")
        for i in range(0,len(x)+1-n):
            out[x[i:i+n]] = 1
        return out
        # END_YOUR_CODE

    return extract


############################################################
# Problem 3e:

def testValuesOfN(n: int):
    '''
    Use this code to test different values of n for extractCharacterFeatures
    This code is exclusively for testing.
    Your full written solution for this problem must be in sentiment.pdf.
    '''
    trainExamples = readExamples('polarity.train')
    validationExamples = readExamples('polarity.dev')
    featureExtractor = extractCharacterFeatures(n)
    weights = learnPredictor(trainExamples,
                             validationExamples,
                             featureExtractor,
                             numEpochs=20,
                             eta=0.01)
    outputWeights(weights, 'weights')
    outputErrorAnalysis(validationExamples, featureExtractor, weights,
                        'error-analysis')  # Use this to debug
    trainError = evaluatePredictor(
        trainExamples, lambda x:
        (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    validationError = evaluatePredictor(
        validationExamples, lambda x:
        (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    print(("Official: train error = %s, validation error = %s" %
           (trainError, validationError)))


############################################################
# Problem 5: k-means
############################################################




def kmeans(examples: List[Dict[str, float]], K: int,
           maxEpochs: int) -> Tuple[List, List, float]:
    '''
    Perform K-means clustering on |examples|, where each example is a sparse feature vector.

    examples: list of examples, each example is a string-to-float dict representing a sparse vector.
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxEpochs: maximum number of epochs to run (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments (i.e. if examples[i] belongs to centers[j], then assignments[i] = j),
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (our solution is 28 lines of code, but don't worry if you deviate from this)
    def square_dict(input_dict):
        squared = [0] * len(input_dict)
        for i in range(len(input_dict)):
            sqrd =defaultdict(float)
            for k,v in input_dict[i].items():
                sqrd[k] = v ** 2
            squared[i] = sqrd
        return squared

    def eud(i, cent, cent_sqr):
        dist = sum(squared_examples[i].values()) + sum(cent_sqr.values())
        union_k = examples[i].keys() & cent.keys()
        for k in union_k:
            dist+= -2*(examples[i][k] * cent[k])
        return dist

    centroids = random.sample(list(examples), K)
    squared_examples= square_dict(examples)
    assign_cluster = [0] * len(examples)
    save_assignments = [0] * len(examples)
    distance_v = [0] * len(examples)

    for _ in range(maxEpochs):
        squared_centroid = square_dict(centroids)
        for i in range(len(examples)):
            min_dist = float('inf')
            for c in range(len(centroids)):
                c_dist = eud(i, centroids[c], squared_centroid[c])
                if c_dist < min_dist:
                    min_dist = c_dist
                    assign_cluster[i] = c
                    distance_v[i] = min_dist

        if save_assignments != assign_cluster:
            cluster_size = [0] * len(centroids)
            for c in range(len(centroids)):
                centroids[c] = {key: 0 for key in centroids[c]}

            for i in range(len(examples)):
                cluster_size[assign_cluster[i]] += 1
                cluster = centroids[assign_cluster[i]]
                for k,v in examples[i].items():
                    if k in cluster:
                        cluster[k] = cluster.get(k) + v
            for i, cluster in enumerate(centroids):
                for k in cluster:
                    cluster[k]= cluster[k]/cluster_size[i]
            save_assignments = assign_cluster
        else: #save_assignments != assign_cluster:
            break

    return (centroids,assign_cluster,sum(distance_v))
    # END_YOUR_CODE
