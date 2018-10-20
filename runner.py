from tempfile import NamedTemporaryFile
from subprocess import check_call

def run(template,
        nodes      = 1,
        ppn        = 1,
        save       = False, 
        submit     = False, 
        jobname    = None,
        queue      = 'skx-normal',
        walltime   = None, 
        preproc    = None,
        postproc   = None,
        executable = None):

    # Creates and (optionally) launches slurm job scripts.
    # Inputs: 
    # -- template     : slurm template file to use
    # -- nodes        : Number of nodes to request
    # -- ppn          : Number of processses per node
    # -- save         : Save the generated slurm script? If false, 
    #                   a temporary file is used as the slurm script.
    # -- submit       : Submit the job script? 
    # -- jobname      : Name of the job
    # -- queue        : Queue to submit to
    # -- walltime     : Wall clock time in seconds 
    # -- preproc      : Preprocessing shell script
    # -- postproc     : Postprocessing shell script
    # -- executable   : executable shell script

    
    #Read the slurm template file
    with open(template, 'r') as temp:
        slurm = temp.read()

    #dictionary of inputs to the slurm template string defined above
    slurm_dict = {'preproc'    : preproc,
                  'postproc'   : postproc,
                  'executable' : executable,
                  'nodes'      : nodes,
                  'queue'      : queue,
                  'ppn'        : ppn,
                  'walltime'   : walltime}
    

    slurm_dict['jobname'] = '%s_%02d_%02d' % (jobname, nodes, ppn)

    with open(slurm_dict['jobname'] + '.slurm', 'w') if save \
            else NamedTemporaryFile(prefix=d['jobname']) as f:
        print(slurm_dict)
        f.write((slurm) % slurm_dict)
        f.flush()

        #submit job if necessary
        if submit:
            check_call(['sbatch', f.name])


