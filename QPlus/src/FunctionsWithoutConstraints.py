
from decimal import Decimal

###########################################################################
#                        Elementary functions                             #
###########################################################################
def compute_Cnk(maxItemsetLength):
    cnk_matrix = [[1]]
    for i in range(1, maxItemsetLength + 1):
        cnk_matrix.append([1] + [cnk_matrix[i - 1][min(i - k, k - 1)] + cnk_matrix[i - 1][min(i - 1 - k, k)] for k in range(1, int(i / 2) + 1)])
    return cnk_matrix

def computeCnk(j, l, cnk_matrix):
    if l > j or l<0:
        return 0
    return cnk_matrix[j][min(j - l, l)]

def find(tab, i, j, x):
    m = int((i + j) / 2)
    if m == 0 or (tab[m - 1] < x and x <= tab[m]):
        return m
    if tab[m] < x:
        return find(tab, m + 1, j, x)
    return find(tab, i, m, x)

def find_index(x, j, i, cnk_matrix, l, wtrans, agg_util):
    m = int((j + i) / 2)
    b_sup = (Decimal(wtrans[m][1]) + agg_util) * computeCnk(m, l - 1, cnk_matrix)
    b_inf = (Decimal(wtrans[m - 1][1]) + agg_util) * computeCnk(m - 1, l - 1, cnk_matrix)
    if b_inf < x and x <= b_sup:
        return m
    if b_sup < x:
        return find_index(x, m + 1, i, cnk_matrix, l, wtrans, agg_util)
    return find_index(x, j, m, cnk_matrix, l, wtrans, agg_util)


###########################################################################
#                        Weighting algorithm                              #
###########################################################################


def computeWeightDatasetWithoutConstraint(data):
    weights = []
    z = Decimal(0)
    for infotrans in data:
        z += 2**(infotrans[0] - 1) + Decimal(infotrans[1])
        weights.append(z)
    return weights


def computeWeightDatasetWithoutConstraintInMemory(data):
    weights = []
    z = Decimal(0)
    for trans in data:
        z += 2 ** (len(trans) - 1) + Decimal(trans[-1][1])
        weights.append(z)
    return weights

