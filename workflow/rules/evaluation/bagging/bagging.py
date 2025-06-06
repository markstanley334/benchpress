#!/usr/bin/env python3
import numpy as np
import pandas as pd
import sys
import os

# Snakemake injects these for you:
adjs = snakemake.input
bag_value = snakemake.params.bag_value
out_csv = snakemake.output[0]

# 1. Load all adjacency matrices into a list of DataFrames
mats = [pd.read_csv(path, index_col=0) for path in adjs]

# The null bagging case will not happen here, as in the Snakefile we check that bag_params is not None
if bag_value == "standard":
    weights = [1/len(mats)] * len(mats)
    threshold = 0.5
else:
    # bag_cfg == ["weighted", {"threshold":t}, {"id1":w1, ...}]
    _, thr_obj, weight_obj = bag_value
    weights = []
    threshold = thr_obj["threshold"]

    # I don't think this is correct, we can get the name with splicing adjmat=/NAMEHERE/, then maybe some function to get id from name and get weight from weight_obj
    for path in adjs:
        seed = os.path.basename(path).split("seed=")[-1].split("/")[0]
        weights.append(weight_obj.get(seed, 0))

    for i in range(len(weights)):
        weights[i] = weights[i] / sum(weights)


# 3. Compute weighted average adjacency
stack = np.stack([df.values for df in mats], axis=2)
avg_mat = np.tensordot(stack, weights, axes=([2], [0]))

# 4. Threshold to binary edges
bin_mat = (avg_mat >= threshold).astype(int)

# 5. Save back out
pd.DataFrame(bin_mat, index=mats[0].index, columns=mats[0].columns) \
  .to_csv(out_csv)
