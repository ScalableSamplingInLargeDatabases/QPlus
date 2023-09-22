__author__ = ""

import time
from FunctionsWithoutConstraints import computeWeightDatasetWithoutConstraintInMemory, compute_Cnk
from inMemory.InMemoryInfoForProcess import load_dataset_inMemory
from inMemory.InMemorySampling import drawPatternWithoutConstraints

###########################################################################
#                            main function                                #
###########################################################################


def QPlusInMemoryWithoutConstraint(dataset, delim, N):
        data, maxItemsetLength = load_dataset_inMemory(dataset, delim)

        beginTime = time.time()
        cnk_matrix = compute_Cnk(maxItemsetLength)
        weights = computeWeightDatasetWithoutConstraintInMemory(data)
        preprocessingTime = time.time() - beginTime
        
        sampledPatterns = {}
        beginTime = time.time()
        for _ in range(N):
            pattern = drawPatternWithoutConstraints(data, weights, cnk_matrix)
            if pattern in sampledPatterns.keys():
                sampledPatterns[pattern] += 1
            else:
                sampledPatterns[pattern] = 1
        samplingTime = time.time() - beginTime
        
        return sampledPatterns, preprocessingTime, samplingTime

