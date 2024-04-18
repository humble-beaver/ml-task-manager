"""Slurm Job Manager wrapper module"""
import subprocess
import time
import os


class SlurmJobCaller:
    """Slurm Job Caller Class, responsible for a single job.
    """

    def __init__(self, code_path, num_instances, sif_path, share_dir,
                 input_folder, output_folder,
                 slurm_queue, slurm_account):
        self.code_path = code_path
        self.num_instances = num_instances
        self.sif_path = sif_path
        self.share_dir = share_dir
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.slurm_queue = slurm_queue
        self.slurm_account = slurm_account
        self.job_id = None
        self.gres = '--gres=gpu:1' if 'gpu' in slurm_queue else ''

    def __read_template(self, template_path):
        with open(template_path, "r", encoding='utf-8') as f:
            template = f.read()
        return template

    def cancel_job(self):
        """Cancel the running job
        """
        if not self.job_id:
            print("There is no job running!")
            return

        try:
            subprocess.run(['ssh', 'atn1mg4', 'scancel',
                           str(self.job_id)], check=True)
            print(f"Job {self.job_id} cancelled successfully.")

        except subprocess.CalledProcessError as e:
            print(f"Error cancelling job {self.job_id}: {e}")

    def submit_and_wait(self, debug_messages=False):
        """Submit job and wait response synchronously

        :param debug_messages: Prints 'job still running', defaults to False
        :type debug_messages: bool, optional
        :return: nothing, just 1
        :rtype: int
        """
        self.submit_job()

        if not self.job_id:
            print("Error submitting job.")

        while self.get_job_status() in ['R', 'PD', 'CG']:
            if debug_messages:
                print("Job still running...")
            time.sleep(10)

        print(f"Job {self.job_id} has finished.")
        return 1

    def submit_job(self):
        """Submit job asynchronously

        :raises Exception: if subprocess execution fails
        :return: slurm job ID returned by sbatch call, or -1 if running
        :rtype: int
        """
        if self.job_id:
            print(f"Job is already running. Job id is {self.job_id}")
            return -1

        slurm_template = self.__read_template("./slurm_template.srm")

        slurm_script = slurm_template.format(
            slurm_queue=self.slurm_queue,
            slurm_account=self.slurm_account,
            num_instances=self.num_instances,
            gres=self.gres,
            sif_path=self.sif_path,
            share_dir=self.share_dir,
            code_path=self.code_path,
            input_folder=self.input_folder,
            output_folder=self.output_folder
        )

        slurm_script_path = os.path.join(
            self.output_folder, os.path.join(self.output_folder,
                                             "job_script.srm"))
        with open(slurm_script_path, "w", encoding="utf-8") as f:
            f.write(slurm_script)

        try:
            submit_command = f"ssh atn1mg4 sbatch - -export = ALL \
                {slurm_script_path}"
            output = subprocess.check_output(submit_command, shell=True)
        except Exception as e:  # TODO: Check possible exceptions
            raise Exception(f"Error submitting job: {e}") from e

        self.job_id = int(output.decode().strip().split()[-1])
        print(f"Job submitted succesfully. Job id is: {self.job_id}")
        return self.job_id

    def get_job_status(self):
        """Get Job status via squeue command

        :return: output of squeue command with job_id specified TODO: specify
        :rtype: str
        """
        if self.job_id is None:
            print("Warning: No job submitted yet.")
        else:
            try:
                squeue_command = f"ssh atn1mg4 squeue -j {self.job_id}"
                output = subprocess.check_output(squeue_command, shell=True)
                status = output.decode().splitlines()[1].split()[4]
                return status
            except subprocess.CalledProcessError:
                print(f"Job {self.job_id} not found.")
            except Exception: # TODO: Check possible exceptions
                if self.job_id:
                    print("Job has already finished.")
        return None
