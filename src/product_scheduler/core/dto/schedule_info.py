from dataclasses import dataclass, field

from product_scheduler.core.dto.element_infos.operation_info import OperationInfo

from . import ResourceGroupInfo, ResourceInfo, JobInfo, OperationInfo


@dataclass
class ScheduleInfo:
    resource_group_infos: list[ResourceGroupInfo]
    resource_infos: list[ResourceInfo]
    job_infos: list[JobInfo]
    operation_infos: list[OperationInfo]
