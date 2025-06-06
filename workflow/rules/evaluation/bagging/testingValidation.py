import sys
import json
import os

# this file is for validating the bagging length function

# syntax to run: python testingValidation.py --configfile bagging_config.json
# print("--------------------------------")
# print("Starting bagging length validation...")
# print("--------------------------------")
# print("--------------------------------")


# def validate_bagging_lengths(config):
#     """
#     Ensure that any weighted‐bagging entry has exactly one weight per
#     algorithm listed in graph_estimation.ids for its benchmark_setup.
#     """
#     bmark = config["benchmark_setup"][0]
#     alg_ids = bmark["evaluation"]["graph_estimation"]["ids"]
#     n_algs = len(alg_ids)

#     print("--------------------------------")
#     print(f"Number of algorithms: {n_algs}")
#     print("--------------------------------")

#     bag = bmark["evaluation"]["bagging"]

#     print("--------------------------------")
#     print(f"Bagging: {bag}")
#     print("--------------------------------")

#     for item in bag:
#         print(f"Item: {item}")
#         if isinstance(item, dict) and "threshold" not in item:
#             # this is the weighted bagging case, so we verify that the length of the bagging dictionary is the number of algorithms
#             print(f"Weighted bagging case: {bag}")
#             if len(item) != n_algs:
#                 raise ValueError(
#                     f"ERROR: Weighted bagging has {len(item)} weights but there are {n_algs} algorithms in the ids field! Check your config file."
#                 )

#     # Also ensure the keys exactly match the alg IDs
#     # simple set difference will be empty if identical string values
#     # not worried about extra keys, as the length is already checked
#             missing = set(alg_ids) - set(item.keys())

#             if missing:
#                 raise ValueError(
#                     f"ERROR: Weighted bagging keys do not match the alg IDs! Check your config file."
#                 )
#     # If we reach here, everything's OK.
#     print("--------------------------------")
#     print("ALL TESTS PASSED")
#     print("--------------------------------")
#     return


def validate_bagging_lengths(config):
    """
    Ensures that the bagging length is the same as the number of algorithms and that the keys exactly match the alg IDs
    """
    bmark = config["benchmark_setup"][0]
    alg_ids = bmark["evaluation"]["graph_estimation"]["ids"]
    n_algs = len(alg_ids)
    bag = bmark["evaluation"]["bagging"]

    if isinstance(bag, list):
        for item in bag:
            if isinstance(item, dict) and "threshold" not in item:
                # this is the weighted bagging case, so we verify that the length of the bagging dictionary is the number of algorithms
                if len(item) != n_algs:
                    raise ValueError(
                        f"ERROR: Weighted bagging has {len(item)} weights but there are {n_algs} algorithms in the ids field! Check your config file."
                    )

        # Also ensure the keys exactly match the alg IDs. A simple set difference will be empty if identical string values.
        # We are not worried about extra keys, as the length is already checked
                missing = set(alg_ids) - set(item.keys())

                if missing:
                    raise ValueError(
                        f"ERROR: Weighted bagging keys do not match the alg IDs! Check your config file."
                    )
    # If we reach here, everything's OK.
    print("--------------------------------")
    print("ALL TESTS PASSED")
    print("--------------------------------")
    return


# command line arguments:

args = sys.argv
configfilename = "config/config.json"
i = 0
for arg in args:
    if arg == "--configfile" or arg == "--configfiles":  # This is strange
        configfilename = args[i + 1]
        break
    i += 1
# print("--------------------------------")
# print(f"Using config file: {configfilename}")
# print("--------------------------------")


with open(configfilename) as json_config:
    cf = json.load(json_config)
    # print("--------------------------------")
    # print(cf)
    # print("--------------------------------")
    validate_bagging_lengths(cf)


#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################


# ["weighted",{"threshold":0.7},{"sampleID":5,"sampleID2":6}]
