__author__ = ""

import time
from FunctionsWithConstraints import computeWeightDatasetWithConstraintOnDisk, compute_Cnk
from OnDisk.OnDiskInfoForProcess import load_dataset_OnDisk
from OnDisk.OnDiskSampling import drawPatternOnDiskWithConstraint

###########################################################################
#                            main function                                #
###########################################################################


def QPlusOnDiskWithConstraint(dataset, delim, max_Length, N):
    data, maxItemsetLength = load_dataset_OnDisk(dataset, delim)
   
    beginTime = time.time()
    cnk_matrix = compute_Cnk(maxItemsetLength, max_Length)
    weights = computeWeightDatasetWithConstraintOnDisk(data, max_Length, cnk_matrix)
    preprocessingTime = time.time() - beginTime
    
    beginTime = time.time()
    sampledPatterns = drawPatternOnDiskWithConstraint(dataset, data, weights, cnk_matrix, delim, max_Length, N)
    samplingTime = time.time() - beginTime
    
    return sampledPatterns, preprocessingTime, samplingTime

