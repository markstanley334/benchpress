# This is the bagging rule. It takes in the adjmat.csv files and performs bagging over them.
include: "validate.py" # to use idtoalg function

if config["benchmark_setup"][0]["evaluation"]["bagging"] is not None: # we don't want to generate any csv file if bagging is null (rule will not be triggered)
    rule bagging:
        """
        Perform standard or weighted bagging over multiple
        adjacency‐matrix CSVs produced by graph_estimation.
        """
        # Expand all the per‐seed adjmat inputs using the seed_range from your config:
        input:
            expand(matrix_filename="{output_dir}/adjmat_estimate/" # this is all combinations of the adjmat paths
            "adjmat=/{adjmat_string}/"
            "parameters=/{param_string}/"
            "data=/{data_string}/"
            "algorithm=/{alg_string}/"
            "seed={seed}/"
            "adjmat.csv")

        # This wildcard picks up the graph_type from the output path:
        output:
            adjmat="results/evaluation/bagging/bagged_adjmat.csv"

        # Pull in the bagging spec (null / "standard" / weighted array):
        params:
            bag_value=lambda wc, config: config["benchmark_setup"][0]["bagging"]
        # Delegate all the heavy lifting to your Python script
        script:
            "rules/evaluation/bagging/bagging.py"


    rule plot_bagging:
        input:
            adjmat="results/evaluation/bagging/bagged_adjmat.csv"
        output:
            donefile="results/output/"+bmark_setup_title +"/bagging/plot_bagging.done"
            plot="results/evaluation/bagging/bagged_adjmat.png"
        script:
            "rules/evaluation/bagging/plot_bagging.py"