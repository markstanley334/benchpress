# rules/evaluation/bagging/rule.smk
rule bagging:
    """
    Perform standard or weighted bagging over multiple
    adjacency‐matrix CSVs produced by graph_estimation.
    """
    # This wildcard picks up the graph_type from the output path:
    output:
        adjmat="results/evaluation/bagging/graph_type={graph_type}/bagged_adjmat.csv"
    # Expand all the per‐seed adjmat inputs using the seed_range from your config:
    input:
        adjs=lambda wc, config: expand(
            "results/evaluation/graph_estimation/graph_type={graph_type}/seed={seed}/adjmat.csv",
            graph_type=wc.graph_type,
            seed=list(range(
                config["benchmark_setup"][0]["data"][0]["seed_range"][0],
                config["benchmark_setup"][0]["data"][0]["seed_range"][1] + 1
            ))
        )
    # Pull in the bagging spec (null / "standard" / weighted array):
    params:
        bag_cfg=lambda wc, config: config["benchmark_setup"][0]["bagging"]
    # Delegate all the heavy lifting to your Python script
    script:
        "rules/evaluation/bagging/bagging.py"