How does the Benchpress workflow work? This file serves as a general documentation file for developers on the software.

See: https://benchpressdocs.readthedocs.io/ for an overview of what benchpress does.

Run, develop, and create benchmarks of structure learning algorithms for probabilistic graphical models.

Benchpress is a Snakemake workflow, a pythonic workflow manager that separates tasks based on output and input files, into a directed acyclic graph, so that tasks unrelated can run in parallel.
The user can decide how many cpu cores to use when running the software.

There are 5 scenarios outlined in the data scenarios section of the website. For the data setup section in the JSON file,
it will look like: "data": [
{
"graph_id": null,
"parameters_id": null,
"data_id": "my_data_file.csv",
"seed_range": null
}
]

where the nulls may be replaced for different types of analysis

The Snakefile is the workflow. Here is what it does:

At the beginning the file runs check_system_requirements(), which ensures that the versions of snakemake, apptainer, etc. are up to date.

The flow sets the configfile: to the passed in config file, located in the /config subfolder.

Schema section:

What Is JSON Schema?
Think of a schema as a blueprint or contract for what valid JSON data should look like. It defines:

- What fields are required
- What types each field should be (string, number, array, etc.)
- What values are allowed (enums, patterns, etc.)
- Nested structures and sub-schemas

So what the workflow does here:

Looks through all of the structure learning algorithms, the graphs, the parameters, the data, and the evaluation to set all the schemas in place.

Once all of these schemas are combined into one schema, the important line here is snakemake.utils.validate(config,tmp_schema), which is what makes sure the provided configfile is valid.

Once this is done the flow needs the docker images to let the software work on any device.

The rule all: section describes the get_active_rules() python function, which will be ran to determine which rules to run. As the function is listed as input, it will run all of the rules that get_active_rules() returns (returns rules based on config file)

Next the flow goes to find the .smk files (rules) that are going to be used. Snakemake wants to run certain rules but they might not yet exist in scope, so the file keeps running and includes all the rules specified in the config file.

Once all the rules are in the document, the flows will run in the desired order, the data will be generated, the structure algorithms will run on generated or provided data with the proper parameters, then all the plots will be generated.

With this, if there are edge constraints they will be applied to make the output correct.

After the edge constraints step, the bagging function will work. Once the rule is triggered, the new csv files are used as input (one for each structure learning algorithm), then the script bagging.py uses all this input and produces the desired result.
