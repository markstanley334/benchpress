#!/usr/bin/env python3
import pandas as pd
import sys
import os

# Snakemake injects these for you:
adjs = snakemake.input.adjs
bag_cfg = snakemake.params.bagging
out_csv = snakemake.output[0]

# 1. Load all adjacency matrices into a list of DataFrames
mats = [pd.read_csv(path, index_col=0) for path in adjs]

# 2. Decide on weights & threshold
if bag_cfg is None:
    # No bagging: just copy the first
    result = mats[0]
elif bag_cfg == "standard":
    weights = [1/len(mats)] * len(mats)
    threshold = 0.5
else:
    # bag_cfg == ["weighted", {"threshold":t}, {"id1":w1, ...}]
    _, thr_obj, weight_obj = bag_cfg
    weights = []
    # match order of `adjs` by their seed IDs (extract from filename)
    for path in adjs:
        seed = os.path.basename(path).split("seed=")[-1].split("/")[0]
        weights.append(weight_obj.get(seed, 0))
    threshold = thr_obj["threshold"]

# 3. Compute weighted average adjacency
import numpy as np
stack = np.stack([df.values for df in mats], axis=2)
avg_mat = np.tensordot(stack, weights, axes=([2], [0]))

# 4. Threshold to binary edges
bin_mat = (avg_mat >= threshold).astype(int)

# 5. Save back out
pd.DataFrame(bin_mat, index=mats[0].index, columns=mats[0].columns) \
  .to_csv(out_csv)