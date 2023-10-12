from decimal import Decimal
from random import random, randint, sample
from FunctionsWithConstraints import computeCnk, find, find_index
from FunctionsWithoutConstraints import find_index as find_indexWithout

###########################################################################
#                        Sampling algorithm                               #
###########################################################################

def draw_length(trans, cnk_matrix, max_Length):
    tabWeigth_len = []
    z = 0
    for l in range(1, min(len(trans), max_Length) + 1):
        z += (trans[-1][1] * computeCnk(len(trans) - 1, l - 1, cnk_matrix)) / l
        tabWeigth_len.append(z)
    return find(tabWeigth_len, 0, len(tabWeigth_len), random() * z)

def drawPatternWithConstraints(data, weights, cnk_matrix, max_Length):
    tid = find(weights, 0, len(weights), random() * weights[-1])
    l = draw_length(data[tid], cnk_matrix, max_Length) + 1
    pattern = []
    i = len(data[tid])
    x = random() * data[tid][i - 1][1] * computeCnk(i - 1, l - 1, cnk_matrix)
    agg_util = 0.
    while l > 0:
        m = find_index(x, l - 1, i, cnk_matrix, l, data[tid], agg_util)
        pattern = [data[tid][m][0]] + pattern
        agg_util += data[tid][m][1]
        if m > 0:
            agg_util -= data[tid][m - 1][1]
        l -= 1
        i = m
        if l > 0:
            x = random() * (data[tid][i - 1][1] + agg_util) * computeCnk(i - 1, l - 1, cnk_matrix)
    return str(pattern)


def draw_lengthWithoutConstraints(trans, cnk_matrix):
    z = Decimal(random()) * (2 ** (len(trans) - 1)) * Decimal(trans[-1][1])
    for l in range(1, len(trans) + 1):
        z -= Decimal(trans[-1][1]) * computeCnk(len(trans) - 1, l - 1, cnk_matrix)
        if z <= 0:
            return l
    return len(trans)


def drawPatternWithoutConstraints(data, weights, cnk_matrix):
    tid = find(weights, 0, len(weights), Decimal(random()) * weights[-1])
    l = draw_lengthWithoutConstraints(data[tid], cnk_matrix)
    pattern = []
    i = len(data[tid])
    x = Decimal(random()) * Decimal(data[tid][i - 1][1]) * computeCnk(i - 1, l - 1, cnk_matrix)
    agg_util = 0
    while l > 0:
        m = find_indexWithout(x, l - 1, i, cnk_matrix, l, data[tid], agg_util)
        pattern = [data[tid][m][0]] + pattern
        agg_util += Decimal(data[tid][m][1])
        if m == l - 1:
            pattern = [data[tid][v][0] for v in range(m)] + pattern
            return str(pattern)
        if m > 0:
            agg_util -= Decimal(data[tid][m - 1][1])
        l -= 1
        i = m
        x = Decimal(random()) * (Decimal(data[tid][m - 1][1]) + agg_util) * computeCnk(m, l - 1, cnk_matrix)
    return str(pattern)


def bootstrapSampling(data, max_Length):
    tid = randint(0, len(data) - 1)
    agg_util = 0.
    pattern = []
    for e in sample(data[tid], randint(1, min(len(data[tid]), max_Length))):
        pattern.append(e[0])
        agg_util += e[1]
    return str(pattern), agg_util / len(pattern)

