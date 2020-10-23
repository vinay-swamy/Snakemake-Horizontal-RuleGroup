# Snakemake-Horizontal-RuleGroup for cluster submission

Snakemake supports vertical rule grouping, where *different rules* with the *same wildcards* will be run in the same job.

Snakemake does **not** support vertical rule grouping, where *different wildcards* of the *same rule* are run in the same job. 

This is an example workflow that(poorly) implements horizontal grouping, for the slurm submission system

How it works:
 - make a dummy rule upstream of the rule you want to create a horizontal group for(target rule). This dummy is a `localrule`, so it will run on the same node the main snakemake job is on.
 - this dummy rule runs `listener.py` which is disowned for from this rule, and dummy output is created. Because `listener.py` is disowned, it will keep running after this rule completes.
 - when target rule runs, `cluster-config.py` writes jobs scripts to a temporary location, instread of submitting it
 - `listner.py` runs in a loop, waiting for all the temporary jobs scripts to be written
 - once all temp jobs scripts have been written, `listener.py` aggregates the scripts into a single script and then submits to the cluster. 
