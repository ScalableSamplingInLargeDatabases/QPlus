__author__ = ""

import time
from FunctionsWithConstraints import computeWeightDatasetWithConstraint, compute_Cnk
from inMemory.InMemoryInfoForProcess import load_dataset_inMemory, load_profile_inMemory
from inMemory.InMemorySampling import drawPatternWithConstraints





###########################################################################
#                            main function                                #
###########################################################################


def QPlusInMemoryWithConstraint(dataset, delim, max_Length, N):
    data, maxItemsetLength = load_dataset_inMemory(dataset, delim)  # loard_profile(dataset)#

    beginTime = time.time()
    cnk_matrix = compute_Cnk(maxItemsetLength, max_Length)
    weights = computeWeightDatasetWithConstraint(data, max_Length, cnk_matrix)
    preprocessingTime = time.time() - beginTime
    
    sampledPatterns = {}
    beginTime = time.time()
    for _ in range(N):
        pattern = drawPatternWithConstraints(data, weights, cnk_matrix, max_Length)
        if pattern in sampledPatterns.keys():
            sampledPatterns[pattern] += 1
        else:
            sampledPatterns[pattern] = 1
    samplingTime = time.time() - beginTime
    
    return sampledPatterns, preprocessingTime, samplingTime



def QPlusInMemoryWithConstraintProfile(dataset, max_Length, N):
    data, maxItemsetLength = load_profile_inMemory(dataset)

    beginTime = time.time()
    cnk_matrix = compute_Cnk(maxItemsetLength, max_Length)
    weights = computeWeightDatasetWithConstraint(data, max_Length, cnk_matrix)
    preprocessingTime = time.time() - beginTime

    sampledPatterns = {}
    beginTime = time.time()
    for _ in range(N):
        pattern = drawPatternWithConstraints(data, weights, cnk_matrix, max_Length)
        if pattern in sampledPatterns.keys():
            sampledPatterns[pattern] += 1
        else:
            sampledPatterns[pattern] = 1
    samplingTime = time.time() - beginTime
    
    return sampledPatterns, preprocessingTime, samplingTime


