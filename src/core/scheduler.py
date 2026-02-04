from typing import Optional

from core.elements.job import Job
from core.elements.resource import ResourceKind, Resource


class Scheduler:
    """
    Jobを内包するクラス.
    Jobとその開始タイムバケットのみを保持する.
    """

    def __init__(self):
        self.root_job = Job(job_id=0, name="root")
        self._jobs: dict[int, Job] = {0: self.root_job}
        self._resource_kinds: dict[int, ResourceKind] = {}
        self._resources: dict[int, Resource] = {}

    @property
    def n_jobs(self):
        return len(self._jobs)

    @property
    def n_resources(self):
        return len(self._resources)

    def add_resource_kind(self, resource_kind: ResourceKind):
        assert (
            not resource_kind.resource_kind_id in self._resources
        ), "resource_kind_id={0}はすでに存在します.".format(
            resource_kind.resource_kind_id
        )
        self._resource_kinds[resource_kind.resource_kind_id] = resource_kind

    def add_resource(self, resource: Resource):
        assert (
            not resource.resource_id in self._resources
        ), "resource_id={0}はすでに存在します.".format(resource.resource_id)
        self._resources[resource.resource_id] = resource

    def add_job(self, job: Job):
        assert not job.job_id in self._jobs, "job_id={0}はすでに存在します.".format(
            job.job_id
        )
        self._jobs[job.job_id] = job

    def create_job(self, name, parent_job: Optional[Job]):
        if self._jobs:
            new_id = max(self._jobs.keys()) + 1
        else:
            new_id = 1

        target_job = parent_job if parent_job is not None else self.root_job

        new_job = Job(job_id=new_id, name=name, parent=target_job)

        self._jobs[new_id] = new_job
