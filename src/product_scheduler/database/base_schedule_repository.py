from abc import ABC, abstractmethod

from product_scheduler.core.dto import (
    ScheduleInfo,
    ResourceGroupInfo,
    ResourceInfo,
    JobInfo,
    OperationInfo,
)


class BaseScheduleRepository(ABC):

    def __init__(self):
        pass

    def fetch_all_data(self) -> ScheduleInfo:

        # 各infosを取得する
        resource_infos = self._load_resource_infos()
        resource_group_infos = self._load_resource_group_infos()
        job_infos = self._load_job_infos()
        operation_infos = self._load_operation_infos()

        schedule_info = ScheduleInfo(
            resource_group_infos=resource_group_infos,
            resource_infos=resource_infos,
            job_infos=job_infos,
            operation_infos=operation_infos,
        )
        return schedule_info

    @abstractmethod
    def _load_resource_infos(self) -> list[ResourceInfo]:
        pass

    @abstractmethod
    def _load_resource_group_infos(self) -> list[ResourceGroupInfo]:
        pass

    @abstractmethod
    def _load_job_infos(self) -> list[JobInfo]:
        pass

    @abstractmethod
    def _load_operation_infos(self) -> list[OperationInfo]:
        pass
