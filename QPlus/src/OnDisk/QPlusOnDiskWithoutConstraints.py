__author__ = ""

import time
from FunctionsWithoutConstraints import computeWeightDatasetWithoutConstraint, compute_Cnk
from OnDisk.OnDiskInfoForProcess import load_dataset_OnDisk
from OnDisk.OnDiskSampling import drawPatternOnDiskWithoutConstraint

###########################################################################
#                            main function                                #
###########################################################################

def QPlusOnDiskWithoutConstraint(dataset, delim, N):
    data, maxItemsetLength = load_dataset_OnDisk(dataset, delim)

    beginTime = time.time()
    cnk_matrix = compute_Cnk(maxItemsetLength)
    weights = computeWeightDatasetWithoutConstraint(data)
    preprocessingTime = time.time() - beginTime
    
    beginTime = time.time()
    sampledPatterns = drawPatternOnDiskWithoutConstraint(dataset, data, weights, cnk_matrix, delim, N)
    samplingTime = time.time() - beginTime
    
    return sampledPatterns, preprocessingTime, samplingTime 

