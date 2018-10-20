#Script to create and launch batch job scripts for weak and 
#strong scaling analysis of firedrake.

import argparse
from runner import run

preproc_cmd = \
'''
module purge
module load firedrake
source $ACTIVATE_SCRIPT

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
'''

exec_template =  \
'''
ibrun python %(script)s --save_timings %(args)s | tee $LOGFILE
'''

template    = 'sbatch_template'
save        = True
submit      = True

script      = 'firedrake_poisson.py'
mesh_sizes  = {'strong' : {1 : 80, 2 : 80, 3 : 80}, 
               'weak'   : {1 : 40, 2 : 20, 3 : 13}}


##intra node strong scaling
# poly degree 3
nodes        = 1
np           = [1, 3, 6, 12, 24, 48]
scaling_type = 'strong'
deg          = 1
walltime     = {1 : 900, 3 : 600, 6 : 600, 12 : 600, 24 : 600, 48 : 500}

args = ['--n %d' %  mesh_sizes[scaling_type][deg], \
        '--scaling_type %s' % scaling_type, \
        '--poly_degree %d' % deg]


exec_cmd = exec_template % {'script' : script, \
                            'args'   : ' '.join(args)}

postproc_cmd = ''

jobname = 'n_%d_deg_%d_scal_%s' % \
              (mesh_sizes[scaling_type][deg], deg, scaling_type)

for ppn in np:
    run(template,
        nodes      = nodes,
        ppn        = ppn,
        save       = save, 
        submit     = submit, 
        jobname    = jobname,
        walltime   = walltime[ppn],
        preproc    = preproc_cmd,
        postproc   = postproc_cmd,
        executable = exec_cmd)
            
num_nodes = [2, 4, 8, 16, 32]
ppn       = 48
walltime  = {48 : 600}

#inter node scaling
for nodes in num_nodes:
    
    run(template,
        nodes      = nodes,
        ppn        = ppn,
        save       = save, 
        submit     = submit, 
        jobname    = jobname,
        walltime   = walltime[ppn], 
        preproc    = preproc_cmd,
        executable = exec_cmd)
         
