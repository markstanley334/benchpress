# This is the bagging rule. It takes in the adjmat.csv files and performs bagging over them.
# include: "../../validate.py" # to use idtoalg function
print("--------------------------------")
print("BAGGING RULE")
print("--------------------------------")


# maybe include the filenames.py here? (should be included already)
include: "../graph_plots/filenames.py"

bmark_setup = config["benchmark_setup"][0]
bmark_setup_title = bmark_setup["title"]

# def adjmats():

#     ret = expand("{output_dir}/adjmat_estimate/adjmat=/{adjmat_string}/parameters=/{param_string}/data=/{data_string}/algorithm=/{alg_string}/seed={seed}/adjmat.csv")
#     # ret = [[[[expand("{output_dir}/adjmat_estimate/adjmat=/{adjmat_string}/parameters=/{param_string}/data=/{data_string}/algorithm=/{alg_string}/seed={seed}/adjmat.csv",
#     #         output_dir="results",
#     #         alg_string=json_string[alg_conf["id"]],
#     #         **alg_conf,
#     #         seed=seed,
#     #         adjmat_string=gen_adjmat_string_from_conf(sim_setup["graph_id"], seed), 
#     #         param_string=gen_parameter_string_from_conf(sim_setup["parameters_id"], seed),
#     #         data_string=gen_data_string_from_conf(sim_setup["data_id"], seed, seed_in_path=False))
#     # ]]]]
#             # for seed in get_seed_range(sim_setup["seed_range"])]
#             # for sim_setup in config["benchmark_setup"]["data"]]
#             # for alg_conf in config["resources"]["structure_learning_algorithms"][alg] 
#                 #if alg_conf["id"] in config["benchmark_setup"]["evaluation"]["graph_plots"]["ids"]]
#             # for alg in active_algorithms("graph_plots")]
    
#     return ret

if config["benchmark_setup"][0]["evaluation"]["bagging"] is not None: # we don't want to generate any csv file if bagging is null (rule will not be triggered)
    rule bagging:
        """
        Perform standard or weighted bagging over multiple
        adjacency‐matrix CSVs produced by graph_estimation.
        """
        # Expand all the per‐seed adjmat inputs using the seed_range from your config:
        input:
            csv_adjmats = adjmats(bmark_setup)

        # This wildcard picks up the graph_type from the output path:
        output:
            adjmat="results/evaluation/bagging/"+bmark_setup_title+"/bagged_adjmat.csv"

        # Pull in the bagging spec (null / "standard" / weighted array):
        params:
            bag_value=lambda wc, config: config["benchmark_setup"][0]["evaluation"]["bagging"]
        # Delegate all the heavy lifting to your Python script
        script:
            "bagging.py"


    rule heatmap_bagging: # this gets the heatmap
        input:
            matrix_filename="results/evaluation/bagging/"+bmark_setup_title+"/bagged_adjmat.csv"
        output:
            plot_filename="results/evaluation/bagging/"+bmark_setup_title+"/bagged_adjmat.png"
        script:
            "../graph_plots/plot_matrix_as_heatmap.py"


    # not sure where the output for this is.

    # rule graph_bagging: # this gets the graph
    #     input:
    #         matrix_filename="results/evaluation/bagging/"+bmark_setup_title+"/bagged_adjmat.csv"
    #     output:
    #         plot_filename="results/evaluation/bagging/"+bmark_setup_title+"/bagged_graph.png"
    #     script:
    #         "../graph_plots/plot_matrix_as_graph.py"


    rule complete_bagging:
        input:
            # "results/evaluation/bagging/"+bmark_setup_title+"/bagged_graph.png",
            "results/evaluation/bagging/"+bmark_setup_title+"/bagged_adjmat.png"
        output:
            donefile="results/output/"+bmark_setup_title +"/bagging/bagging.done"
        shell:
            """
            touch {donefile}
            echo {donefile}
            """