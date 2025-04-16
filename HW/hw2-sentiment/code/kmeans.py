import submission, util
from collections import defaultdict
from typing import List, Dict, Tuple
import random
from util import generateClusteringExamples


def kmeans(examples: List[Dict[str, float]], K: int,
           maxEpochs: int) -> Tuple[List, List, float]:

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
                    assign_cluster[i], distance_v[i] = c, min_dist

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

def old_kmeans(examples, K, maxIters):
    centroids=[sample.copy() for sample in random.sample(examples,K)]
    bestmatch=[random.randint(0,K-1) for item in examples]
    distances=[0 for item in examples]
    pastmatches=None
    examples_squared=[]
    for item in examples:
        tempdict=defaultdict(float)
        for k,v in item.items():
            tempdict[k]=v*v
        examples_squared.append(tempdict)
    for run_range in range(maxIters):
        centroids_squared=[]
        for item in centroids:
            tempdict = defaultdict(float)
            for k, v in item.items():
                tempdict[k] = v * v
            centroids_squared.append(tempdict)
        for index,item in enumerate(examples):
            min_distance=999999
            for i,cluster in enumerate(centroids):
                distance=sum(examples_squared[index].values())+sum(centroids_squared[i].values())
                #for k in set(item.keys() & cluster.keys()):
                for k in (item.keys() & cluster.keys()):
                    distance+=-2*item[k]*cluster[k]
                if distance<min_distance:
                    min_distance=distance
                    bestmatch[index]=i
                    distances[index]=min_distance
        if pastmatches==bestmatch:
            break
        else:
            clustercounts=[0 for cluster in centroids]
            for i,cluster in enumerate(centroids):
                for k in cluster:
                    cluster[k]=0.0
            for index,item in enumerate(examples):
                clustercounts[bestmatch[index]]+=1
                cluster=centroids[bestmatch[index]]
                for k,v in item.items():
                    if k in cluster:
                        cluster[k]+=v
                    else:
                        cluster[k]=0.0+v
            for i, cluster in enumerate(centroids):
                for k in cluster:
                    cluster[k]/=clustercounts[i]
            pastmatches=bestmatch[:]

    print("centroids", centroids)
    #print("squared_examples", examples_squared)
    print(distances)
    return (centroids,bestmatch,sum(distances))


# basic test for k-means
def test5b0():
    random.seed(42)
    x1 = {0:0, 1:0}
    x2 = {0:0, 1:1}
    x3 = {0:0, 1:2}
    x4 = {0:0, 1:3}
    x5 = {0:0, 1:4}
    x6 = {0:0, 1:5}
    examples = [x1, x2, x3, x4, x5, x6]
    examples = generateClusteringExamples(10, 3,4)
    for ex in examples:
        print(list(ex.keys()), list(ex.values()))
    #centers, assignments, totalCost = old_kmeans(examples, 2, 3)
    #print("centers=", centers, "assignments", assignments)
    #print("cost ", totalCost)
    #print("---------------------------")
    centers, assignments, totalCost = kmeans(examples, 2, 10)
    print("centers=", centers, "assignments", assignments)
    print("cost ", totalCost)

test5b0()