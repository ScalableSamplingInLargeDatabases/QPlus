
from random import random, randint, sample
from decimal import Decimal
from FunctionsWithoutConstraints import computeCnk, find, find_index

###########################################################################
#                        Sampling algorithm                               #
###########################################################################



def drawLength(trans, cnk_matrix):
    x = Decimal(random()) * (2**(trans[0]-1)) * Decimal(trans[1])
    for l in range(1, trans[0]+1):
        x -= Decimal(trans[1])*computeCnk(trans[0]-1, l-1, cnk_matrix)
        if x<=0:
            return l
    return trans[0]

def selectTransIndex(data, weights, cnk_matrix, N):
    selectedTid = {}
    for _ in range(N):
        tid = find(weights, 0, len(weights), Decimal(random()) * weights[-1])
        l = drawLength(data[tid], cnk_matrix)
        if tid in selectedTid.keys():
            selectedTid[tid].append(l)
        else:
            selectedTid[tid] = [l]
    return selectedTid

def drawPatternOnDiskWithoutConstraint(dataset, data, weights, cnk_matrix, delim, N):
    return getPatterns(dataset, cnk_matrix, delim, N, selectTransIndex(data, weights, cnk_matrix, N))


def getPatterns(dataset, cnk_matrix, delim, N, selectedTid):
    sampledPatterns = {}
    tid = 0
    count_patterns = 0
    with open(dataset, 'r') as base:
        line = base.readline()
        while line and count_patterns < N:
            if tid in selectedTid.keys():
                utrans = []
                z = 0
                for e in line.split():
                    e = e.split(delim)
                    z += Decimal(e[1])
                    utrans.append([e[0], z])
                for l in selectedTid[tid]:
                    pattern = []
                    i = len(utrans)
                    x = Decimal(random()) * utrans[i - 1][1] * computeCnk(i - 1, l - 1, cnk_matrix)
                    agg_util = 0
                    while l > 0:
                        m = find_index(x, l - 1, i, cnk_matrix, l, utrans, agg_util)
                        pattern = [utrans[m][0]] + pattern
                        agg_util += utrans[m][1]
                        if m > 0:
                            agg_util -= utrans[m - 1][1]
                        l -= 1
                        i = m
                        if l > 0:
                            x = Decimal(random()) * (utrans[i - 1][1] + agg_util) * computeCnk(i - 1, l - 1, cnk_matrix)
                    pattern = str(pattern)
                    if pattern in sampledPatterns.keys():
                        sampledPatterns[pattern] += 1
                    else:
                        sampledPatterns[pattern] = 1
                count_patterns += len(selectedTid[tid])
                if count_patterns == N:
                    break
            line = base.readline()
            tid += 1
        base.close()
    return sampledPatterns


def draw_length(infotrans, cnk_matrix, max_Length):
    tabWeigth_len = []
    z = 0
    for l in range(1, min(infotrans[0], max_Length) + 1):
        z += (infotrans[1] * computeCnk(infotrans[0] - 1, l - 1, cnk_matrix)) / l
        tabWeigth_len.append(z)
    return find(tabWeigth_len, 0, len(tabWeigth_len), random() * z)


def selectTransIndexWithConstraints(data, weights, cnk_matrix, max_Length, N):
    selectedTid = {}
    for _ in range(N):
        tid = find(weights, 0, len(weights), Decimal(random())* weights[-1])
        l = draw_length(data[tid], cnk_matrix, max_Length)
        if tid in selectedTid.keys():
            selectedTid[tid].append(l)
        else:
            selectedTid[tid] = [l]
    return selectedTid


def drawPatternOnDiskWithConstraint(dataset, data, weights, cnk_matrix, delim, max_Length, N):
    return getPatterns(dataset, cnk_matrix, delim, N, selectTransIndexWithConstraints(data, weights, cnk_matrix, max_Length, N))


def bootstrapSampling(data, max_Length):
    tid = randint(0, len(data) - 1)
    return str([e[0] for e in sample(data[tid], randint(1, min(len(data[tid]), max_Length)))])
