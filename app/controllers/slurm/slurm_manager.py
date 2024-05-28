"""Slurm Job Manager for job instanciation controll
"""
from ...utils import save_file


def read_template(template_path):
    """read template file"""
    with open(template_path, "r", encoding='utf-8') as f:
        template = f.read()
    return template


def prep_template(job_params):
    """Prepare template with job parameters"""
    template = read_template("app/controllers/slurm/slurm_template.srm")
    slurm_script = template.format(
        experiment_name=job_params['experiment_name'],
        instance_type=job_params['instance_type'],
        account=job_params['account'],
        image_name=job_params['image_name'],
        train_script_path=job_params['train_script_path'],
        dataset_name=job_params['dataset_name']
    )
    fname = 'slurm_script.srm'
    save_file(fname, slurm_script)
    return fname
