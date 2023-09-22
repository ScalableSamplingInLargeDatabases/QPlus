
from decimal import Decimal

###########################################################################
#                        Elementary functions                             #
###########################################################################


def compute_Cnk(maxItemsetLength, max_Length):
    cnk_matrix = [[1]]
    for i in range(1, maxItemsetLength + 1):
        cnk_matrix.append([1] + [cnk_matrix[i - 1][k - 1] + cnk_matrix[i - 1][min(i - 1 - k, k)] for k in range(1, min(max_Length, int(i / 2)) + 1)])
        #cnk_matrix[i].append(1)
    return cnk_matrix

def computeCnk(j, l, cnk_matrix):
    if l > j:
        return 0
    if l > j / 2:
        return cnk_matrix[j][j - l]
    return cnk_matrix[j][l]

def find(tab, i, j, x):
    m = int((i + j) / 2)
    if m == 0 or (tab[m - 1] < x and x <= tab[m]):
        return m
    if tab[m] < x:
        return find(tab, m + 1, j, x)
    return find(tab, i, m, x)

def find_index(x, j, i, cnk_matrix, l, wtrans, agg_util):
    m = int((j + i) / 2)
    b_sup = (wtrans[m][1] + agg_util) * computeCnk(m, l - 1, cnk_matrix)
    b_inf = (wtrans[m - 1][1] + agg_util) * computeCnk(m - 1, l - 1, cnk_matrix)
    if b_inf < x and x <= b_sup:
        return m
    if b_sup < x:
        return find_index(x, m + 1, i, cnk_matrix, l, wtrans, agg_util)
    return find_index(x, j, m, cnk_matrix, l, wtrans, agg_util)


###########################################################################
#                        Weighting algorithm                              #
###########################################################################

def computeWeightDatasetWithConstraint(data, max_Length, cnk_matrix):
    weights = []
    z = 0
    for trans in data:
        i = len(trans)
        for l in range(1, min(i, max_Length) + 1):
            z += (trans[i - 1][1] * computeCnk(i - 1, l - 1, cnk_matrix)) / l
        weights.append(z)
    return weights

def computeWeightDatasetWithConstraintOnDisk(data, max_Length, cnk_matrix):
    weights = []
    z = Decimal(0)
    for infotrans in data:
        for l in range(1, min(infotrans[0], max_Length) + 1):
            z += (Decimal(infotrans[1])* computeCnk(infotrans[0] - 1, l - 1, cnk_matrix)) / l
        weights.append(z)
    return weights

###########################################################################
#                            statistical function                         #
###########################################################################

def getAverageUtility(data, sampledPatterns):
    statSample = {}
    for trans in data:
        transSet = {}
        x = []
        for e in trans:
            v = 0
            if len(x) != 0:
                v = float(x[1])
            transSet[e[0]] = float(e[1]) - v
            x = e
        for pattern in sampledPatterns:
            patt = set(pattern.replace('[','').replace(']','').replace("'","").split(", "))
            utilPattern = 0
            if patt <= set(transSet.keys()):
                util = 0
                for item in patt:
                    util += transSet[item]
                utilPattern += util
            if pattern in statSample:
                statSample[pattern] += utilPattern / len(patt)
            else:
                statSample[pattern] = utilPattern / len(patt)
    return statSample
