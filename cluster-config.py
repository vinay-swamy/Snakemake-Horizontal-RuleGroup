from snakemake.utils import read_job_properties
import sys
import subprocess as sp
import json
cluster_json_file =sys.argv[1]
jobscript = sys.argv[2]
custom_config_rules = ['job_to_bundle']
with open(cluster_json_file) as j:
    cluster_json = json.load(j)
#%%

params = cluster_json['__default__']
job_properties = read_job_properties(jobscript)
rule = job_properties['rule']
if rule in cluster_json:
    for key in cluster_json[rule]:
        params[key] = cluster_json[rule][key]
elif rule in custom_config_rules:
    # specifify custom configureations specific rules
    print(rule)
    if rule == 'job_to_bundle':
        print(job_properties)
        if job_properties['wildcards']['wc'] == 'Q':
            params = cluster_json['__default__'] 
        else:
            outdir = 'script_temp'
            ec_strings = [f"{key}={job_properties['wildcards'][key]}" for key in job_properties['wildcards'] ]
            ec_strings = '-'.join(ec_strings)
            output = f'{ec_strings}.{rule}.sh'
            sp.run(f"grep -v '#!/bin/sh' {jobscript}  > {outdir}/{output}", shell=True)
            sys.exit()
    
else:# use default parameters
    params = cluster_json['__default__'] 

sbcmd=f'''sbatch --cpus-per-task={params['cpus-per-task']} \
    --mem={params['mem']} \
    --time={params['time']} \
    --job-name={rule} \
    --partition={params['partition']} \
    --output=00log/{rule}.out \
    --error=00log/{rule}.err \
    {params['extra']} \
    {jobscript}

'''
sp.run(sbcmd, shell=True)


