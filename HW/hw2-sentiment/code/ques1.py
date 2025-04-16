#Loss = max { 1 - w.phi(x)y, 0}
#Gradient = -phi(x)y if (1-phi(x).w > 1 else 0
#w = w - 0.1 Gradient(x,y,w)
                        
import submission, util
from collections import defaultdict
trainExamples= {
    ({'not':1, 'good':1}, -1),
    ({'pretty':1, 'bad':1}, -1),
    ({'good':1, 'plot':1}, 1),
    ({'pretty':1, 'scenery':1}, 1),
}
def phi(x):
    words = list(x.values())
    return np.array(words)

#{'pretty':0, 'good':0, 'bad':0, 'plot':0, 'not':0, 'scenery':0}
def initialWeightVector():
    return np.zeros(3)

def gradientHingeLoss(w, i):
    phi, y = trainExamples[i]
    increment()
    return -phi(x) * y if 1 - w.dot(phi(x)) * y > 0 else 0
############################################################
# Optimization algorithm

def stochasticGradientDescent(gradientf, n):
    w = [0] * 6
    eta = 0.1
    for i in range(n):
        gradient = gradientf(w, i)
        w = w - eta * gradient
        print(f'new-w = {w}, gradientF = {gradient}')

stochasticGradientDescent(gradientHingeLoss, len(trainExamples))
