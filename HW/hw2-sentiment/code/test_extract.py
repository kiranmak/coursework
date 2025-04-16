import random
import string
import util
from typing import Callable, Dict, List, Tuple, TypeVar

from util import *

FeatureVector = Dict[str, int]
WeightVector = Dict[str, float]
Example = Tuple[FeatureVector, int]

#def generateDataset(100, weights)
def generateDataset(numExamples: int, weights: WeightVector) -> List[Example]:
    random.seed(42)

    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a score for the given weight vector.
    # note that there is intentionally flexibility in how you define phi.
    # y should be 1 or -1 as classified by the weight vector.
    # IMPORTANT: In the case that the score is 0, y should be set to 1.

    # Note that the weight vector can be arbitrary during testing.
    print( weights)
    def generateExample() -> Tuple[Dict[str, int], int]:
        # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
        keys  = random.sample(list(weights),len(weights))
        phi = {}
        for key in keys:
            phi[key] = random.randint(-10, 10)
        print("phi", phi)
        score = dotProduct(phi, weights)
        y = 1 if score >= 0 else -1
        print("---score", score, "margin=", score * y)
        # END_YOUR_CODE
        return phi, y

    return [generateExample() for _ in range(numExamples)]

def test3c1():
    weights = {}
    count = 5
    for _ in range(5):
        k = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        v = random.uniform(-1, 1)
        weights[k] = v
    data = generateDataset(5, weights)
    for phi, y in data:
        util.dotProduct(phi, weights)# >= 0, y == 1)
    print(weights)
    print("data")
    print(data)

test3c1()