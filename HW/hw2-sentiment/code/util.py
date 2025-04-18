import random
import sys
from collections import Counter
from typing import Callable, Dict, List, Tuple, TypeVar

FeatureVector = Dict[str, int]
WeightVector = Dict[str, float]
Example = Tuple[FeatureVector, int]

T = TypeVar('T')


def dotProduct(d1: Dict, d2: Dict) -> float:
    """
    The dot product of two vectors represented as dictionaries. This function
    goes over all the keys in d2, and for each key, multiplies the corresponding
    values in d1 and d2 and adds the result to a running sum. If the key is not
    in d1, it is treated as having value 0.

    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in list(d2.items()))


def increment(d1: Dict, scale: float, d2: Dict):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in list(d2.items()):
        d1[f] = d1.get(f, 0) + v * scale


def readExamples(path: str):
    '''
    Reads a set of training examples.
    '''
    examples = []
    for line in open(path, "rb"):
        # TODO -- change these files to utf-8.
        line = line.decode('latin-1')
        # Format of each line: <output label (+1 or -1)> <input sentence>
        y, x = line.split(' ', 1)
        examples.append((x.strip(), int(y)))
    print('Read %d examples from %s' % (len(examples), path))
    return examples


def evaluatePredictor(examples: List[Tuple[T, int]], predictor: Callable) -> float:
    '''
    predictor: a function that takes an x and returns a predicted y.
    Given a list of examples (x, y), makes predictions based on |predict| and returns the fraction
    of misclassiied examples.
    '''
    error = 0
    for x, y in examples:
        if predictor(x) != y:
            error += 1
    return 1.0 * error / len(examples)


def outputWeights(weights: WeightVector, path: str):
    print("%d weights" % len(weights))
    out = open(path, 'w', encoding='utf8')
    for f, v in sorted(list(weights.items()), key=lambda f_v: -f_v[1]):
        print('\t'.join([f, str(v)]), file=out)
    out.close()


def verbosePredict(phi: FeatureVector, y: int, weights: WeightVector, out) -> int:
    yy = 1 if dotProduct(phi, weights) >= 0 else -1
    if y:
        print('Truth: %s, Prediction: %s [%s]' % (
            y, yy, 'CORRECT' if y == yy else 'WRONG'), file=out)
    else:
        print('Prediction:', yy, file=out)
    for f, v in sorted(list(phi.items()), key=lambda f_v1: -f_v1[1] * weights.get(f_v1[0], 0)):
        w = weights.get(f, 0)
        print("%-30s%s * %s = %s" % (f, v, w, v * w), file=out)
    return yy


def outputErrorAnalysis(examples: Tuple[FeatureVector, int],
                        featureExtractor: Callable, weights: WeightVector, path: str):
    out = open(path, 'w', encoding='utf-8')
    for x, y in examples:
        print('===', x, file=out)
        verbosePredict(featureExtractor(x), y, weights, out)
    out.close()


def interactivePrompt(featureExtractor: Callable, weights: WeightVector):
    while True:
        print('> ', end=' ')
        x = sys.stdin.readline()
        if not x:
            break
        phi = featureExtractor(x)
        verbosePredict(phi, None, weights, sys.stdout)


############################################################

def generateClusteringExamples(numExamples: int,
                               numWordsPerTopic: int, numFillerWords: int) -> List:
    '''
    Generate artificial examples inspired by sentiment for clustering.
    Each review has a hidden sentiment (positive or negative) and a topic (plot, acting, or music).
    The actual review consists of 2 sentiment words, 4 topic words and 1 filler word, for example:

        good:1 great:1 plot1:2 plot7:1 plot9:1 plot11:1 filler0:1

    numExamples: Number of examples to generate
    numWordsPerTopic: Number of words per topic (e.g., plot0, plot1, ...)
    numFillerWords: Number of words per filler (e.g., filler0, filler1, ...)
    '''
    sentiments = [['bad', 'awful', 'worst', 'terrible'],
                  ['good', 'great', 'fantastic', 'excellent']]
    topics = ['plot', 'acting', 'music']

    def generateExample():
        x = Counter()
        # Choose 2 sentiment words according to some sentiment
        sentimentWords = random.choice(sentiments)
        x[random.choice(sentimentWords)] += 1
        x[random.choice(sentimentWords)] += 1
        # Choose 4 topic words from a fixed topic
        topic = random.choice(topics)
        x[topic + str(random.randint(0, numWordsPerTopic - 1))] += 1
        x[topic + str(random.randint(0, numWordsPerTopic - 1))] += 1
        x[topic + str(random.randint(0, numWordsPerTopic - 1))] += 1
        x[topic + str(random.randint(0, numWordsPerTopic - 1))] += 1
        # Choose 1 filler word
        x['filler' + str(random.randint(0, numFillerWords - 1))] += 1
        return x

    random.seed(42)
    examples = [generateExample() for _ in range(numExamples)]
    return examples


def outputClusters(path: str, examples: List[Dict[str, float]],
                    centers: List, assignments: List):
    '''
    Output the clusters to the given path.
    '''
    print('Outputting clusters to %s' % path)
    out = open(path, 'w', encoding='utf8')
    for j in range(len(centers)):
        print('====== Cluster %s' % j, file=out)
        print('--- Centers:', file=out)
        for k, v in sorted(list(centers[j].items()), key=lambda k_v: -k_v[1]):
            if v != 0:
                print('%s\t%s' % (k, v), file=out)
        print('--- Assigned points:', file=out)
        for i, z in enumerate(assignments):
            if z == j:
                print(' '.join(list(examples[i].keys())), file=out)
    out.close()
