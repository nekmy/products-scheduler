from typing import Optional, List

from product_scheduler.utils.errors.data_integrity_error import DataIntegrityError
from product_scheduler.core.elements.resource_group import ResourceGroup
from product_scheduler.core.elements.resource import Resource
from product_scheduler.core.elements.job import Job
from product_scheduler.core.elements.operation import Operation
from product_scheduler.core.dto.resource_group_info import ResourceGroupInfo
from product_scheduler.core.dto.resource_info import ResourceInfo
from product_scheduler.core.dto.job_info import JobInfo
from product_scheduler.core.dto.operation_info import OperationInfo


class Scheduler:
    """
    Jobを内包するクラス.
    Jobとその開始タイムバケットのみを保持する.
    """

    def __init__(self):
        self._resource_groups: dict[int, ResourceGroup] = (
            {}
        )  # resource_group_id: ResourceGroup
        self._resources: dict[int, Resource] = {}  # redource_id: Resource
        self._jobs: dict[int, Job] = {}  # job_id: Job
        self._operations: dict[int, Operation] = {}  # operation_id: Operation

        # root_jobの格納
        self.root_job = Job(job_id=0, name="root")
        self._jobs[0] = self.root_job

    @property
    def n_jobs(self):
        return len(self._jobs)

    @property
    def n_resources(self):
        return len(self._resources)

    def add_resources(self, resource_infos: List[ResourceInfo]):
        for resource_info in resource_infos:
            # 既にこのidが使用されている場合はエラー
            if resource_info.resource_id in self._resources:
                raise DataIntegrityError()
            resource = Resource(
                resource_id=resource_info.resource_id,
                name=resource_info.name,
                capacity=resource_info.capacity,
            )
            self._resources[resource_info.resource_id] = resource
        return None

    def add_resource_groups(self, resource_group_infos: List[ResourceGroupInfo]):
        """
        resource_kindをインスタンス化して格納する.
        """
        for resource_group_info in resource_group_infos:
            # 既にこのidが使用されている場合はエラー
            if resource_group_info.resource_group_id in self._resource_groups:
                raise DataIntegrityError()
            resource_group = ResourceGroup(
                resource_group_id=resource_group_info.resource_group_id,
                name=resource_group_info.name,
            )
            for resource_id in resource_group_info.resource_ids:
                # resourceが格納されていない場合はエラー
                if resource_id not in self._resources:
                    raise DataIntegrityError()
                resource = self._resources[resource_id]
                resource_group.resources.append(resource)
                resource.resource_groups.append(resource_group)

            # 格納
            self._resource_groups[resource_group_info.resource_group_id] = (
                resource_group
            )
        return None

    def add_jobs(self, job_infos: List[JobInfo]):
        # Jobのインスタンス化
        for job_info in job_infos:
            job = Job(
                job_id=job_info.job_id,
                name=job_info.name,
                need_time_buckets=job_info.need_time_buckets,
            )
            # required_resource_group
            for (
                required_resource_group_id,
                amount,
            ) in job_info.required_resource_group_ids.items():
                required_resource_group = self._resource_groups[
                    required_resource_group_id
                ]
                job.required_resource_groups[required_resource_group] = amount
            self._jobs[job_info.job_id] = job

        # 親子関係の反映
        for job_info in job_infos:
            if job_info.job_id not in self._jobs:
                raise DataIntegrityError()
            if job_info.parent_job_id not in self._jobs:
                raise DataIntegrityError()
            job = self._jobs[job_info.job_id]
            parent_job = self._jobs[job_info.parent_job_id]
            job.parent = parent_job
            parent_job.children.append(job)

        # 前後関係の反映
        for job_info in job_infos:
            if job_info.job_id not in self._jobs:
                raise DataIntegrityError()
            job = self._jobs[job_info.job_id]
            for prev_job_id in job_info.predecessor_job_ids:
                if prev_job_id not in self._jobs:
                    raise DataIntegrityError()
                prev_job = self._jobs[prev_job_id]
                job.predecessors.append(prev_job)
                prev_job.successors.append(job)

        return None

    def add_operations(self, operation_infos: List[OperationInfo]):
        for operation_info in operation_infos:
            operation_id = operation_info.operation_id
            job = self._jobs[operation_info.job_id]
            operation = Operation(
                operation_id=operation_info.operation_id,
                name=operation_info.name,
                job=job,
                sequence_index=operation_info.sequence_num,
            )
            # assigned_resource
            for (
                assigned_resource_id,
                amount,
            ) in operation_info.assigned_resource_ids.items():
                assigned_resource = self._resources[assigned_resource_id]
                operation.assigned_resources[assigned_resource] = amount
            self._operations[operation_id] = operation
            job.operations.append(operation)
        # 親子関係の反映
        for operation_info in operation_infos:
            operation = self._operations[operation_info.operation_id]
            parent_operation = self._operations[operation_info.operation_id]
            operation.parent = parent_operation
            parent_operation.children.append(operation)

        return None

    def create_job(self, name, parent_job: Job):
        if self._jobs:
            new_id = max(self._jobs.keys()) + 1
        else:
            new_id = 1
        target_job = parent_job if parent_job is not None else self.root_job
        new_job = Job(job_id=new_id, name=name, parent=target_job)
        self._jobs[new_id] = new_job
