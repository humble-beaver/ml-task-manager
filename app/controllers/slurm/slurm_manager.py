"""Slurm Job Manager for job instanciation controll
"""
from .slurm_caller import SlurmJobCaller


class SlurmManager:
    """Slurm Job Callers instances controller"""

    def __init__(self):
        self.callers = {}

    def submit_new_job(self, job_params: dict):
        """Submit new job by  spawning new SlurmCaller

        :param job_params: Parameters received by request
        :type job_params: dict
        :return: ID of the new job
        :rtype: int
        """
        new_caller = SlurmJobCaller(**job_params)
        new_job_id = new_caller.submit_job()
        self.callers[new_job_id] = new_caller
        return new_job_id

    def get_job_status(self, job_id):
        """Requests the job status by squeue

        :param job_id: The ID of the job
        :type job_id: int
        :return: filtered squeue command output with job status character
        :rtype: str
        """
        return self.callers[job_id].get_job_status()
