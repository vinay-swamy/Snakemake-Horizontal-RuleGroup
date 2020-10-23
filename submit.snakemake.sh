#!/bin/bash

# to run snakemake as batch job
 module load snakemake || exit 1

# activate conda

rm -rf 00log/
rm -rf script_temp
mkdir -p 00log/ 
mkdir -p script_temp/
snakefile=$1
cluster_json=$2
cluster_config=$3
# activate conda
source ${conda_sh}

snakemake -s $snakefile \
-pr --jobs 1999 \
--cluster "python3 ${cluster_config} ${cluster_json}"  --latency-wait 120 --rerun-incomplete \
-k --restart-times 0 \
--resources parallel=4

