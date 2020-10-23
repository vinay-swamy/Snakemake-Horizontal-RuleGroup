#%%
import sys
import subprocess as sp
import glob
import time 

args = sys.argv 
outdir = args[1]
sfx = args[2]
num_files = int(args[3])
#%%
# outdir = 'script_temp'
# sfx = 'job_to_bundle.sh'
# num_files = 3



# %%
tfiles = []
while len(tfiles) < num_files:
    tfiles = glob.glob( f'{outdir}/*{sfx}', recursive=True)
    print(f'{len(tfiles)} / {num_files} target files detected')
    time.sleep(1)

sp.run(f"echo  '#!/bin/bash' > {sfx}_all.sh ", shell=True)
sp.run(f'cat {outdir}/*{sfx} >> {sfx}_all.sh', shell=True)

# %%
sbcmd=f'''sbatch --cpus-per-task=3 \
    --mem=8G \
    --time=01:00:00 \
    --job-name=job\
    --partition=quick \
    --output=out.out \
    --error=out.err \
    {sfx}_all.sh'''
sp.run(sbcmd, shell=True)