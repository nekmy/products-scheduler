import os
from typing import List

import pandas as pd

from product_scheduler.utils.errors.data_integrity_error import DataIntegrityError
from product_scheduler.core.schedule import Schedule
from product_scheduler.core.dto.element_infos.resource_info import ResourceInfo
from product_scheduler.core.dto.element_infos.resource_group_info import (
    ResourceGroupInfo,
)
from product_scheduler.core.dto.element_infos.job_info import JobInfo
from product_scheduler.core.dto.element_infos.operation_info import OperationInfo


class ScheduleFactory:

    def __init__(self, repository_dir):
        self.repository_dir = repository_dir

    def build(self):
        scheduler = Schedule()

        resource_infos = self._load_resource_infos()
        scheduler._load_resources(resource_infos)

        resource_group_infos = self._load_resource_group_infos()
        scheduler._load_resource_groups(resource_group_infos)

        job_infos = self._load_job_infos()
        scheduler._load_jobs(job_infos)

        operation_infos = self._load_operation_infos()
        scheduler._load_operations(operation_infos)

        return scheduler

    def _load_resource_infos(self):
        resource_infos: List[ResourceInfo] = []
        resources_df = self._read_resources_df()
        for row in resources_df.itertuples():
            resource_info = ResourceInfo(
                resource_id=row.resource_id, name=row.name, capacity=row.capacity
            )
            resource_infos.append(resource_info)
        return resource_infos

    def _load_resource_group_infos(self):
        resource_groups_df = self._read_resource_groups_df()
        resource_group_members_df = self._read_resource_group_members_df()
        resource_group_infos: List[ResourceGroupInfo] = []

        for row in resource_groups_df.itertuples():
            resource_group_info = ResourceGroupInfo(
                resource_group_id=row.resource_group_id, name=row.name
            )
            for resource_id in resource_group_members_df.loc[
                resource_group_members_df.resource_group_id == row.resource_group_id
            ].resource_id:
                resource_group_info.resource_ids.append(resource_id)
            resource_group_infos.append(resource_group_info)

        return resource_group_infos

    def _load_job_infos(self):
        jobs_df = self._read_jobs_df()
        job_order_constraints_df = self._read_job_order_constraints_df()
        job_required_resource_groups_df = self._read_job_required_resource_groups_df()
        operation_assigned_resources_df = self._read_operation_assigned_resources_df()

        job_infos: List[JobInfo] = []

        for row in jobs_df.itertuples():
            job_info = JobInfo(
                job_id=row.job_id,
                name=row.name,
                need_time_buckets=row.need_time_buckets,
                parent_job_id=row.parent_job_id,
            )

            # 前job_idの格納
            for prev_job_id in job_order_constraints_df.loc[
                job_order_constraints_df.job_id == job_info.job_id
            ].prev_job_id:
                job_info.predecessor_job_ids.append(prev_job_id)

            # required_resource_groupの格納
            for required_resource_group in job_required_resource_groups_df.loc[
                job_required_resource_groups_df.job_id == job_info.job_id
            ].itertuples():
                job_info.required_amount_of_resource_group_ids[
                    required_resource_group.resource_group_id
                ] = required_resource_group.amount

            job_infos.append(job_info)

        return job_infos

    def _load_operation_infos(self):
        operations_df = self._read_operations_df()
        operation_assigned_resources_df = self._read_operation_assigned_resources_df()
        operation_infos: List[OperationInfo] = []

        for row in operations_df.itertuples():
            operation_info = OperationInfo(
                operation_id=row.operation_id,
                name=row.name,
                parent_id=row.parent_operation_id,
                operation_type_id=row.operation_type_id,
                sequence_num=row.sequence_num,
                job_id=row.job_id,
            )

            # assigned_resourceの格納
            for assigned_resource in operation_assigned_resources_df.loc[
                operation_assigned_resources_df.operation_id
                == operation_info.operation_id
            ].itertuples():
                operation_info.assigned_amount_of_resource_ids[
                    assigned_resource.resource_id
                ] = assigned_resource.amount

            operation_infos.append(operation_info)

        return operation_infos

    def _read_resources_df(self):
        resources_csv_path = os.path.join(
            self.repository_dir, self.RESOURCES_CSV_FILE_NAME
        )
        resources_df = pd.read_csv(resources_csv_path, encoding="utf-8")
        return resources_df

    def _read_resource_groups_df(self):
        resource_groups_csv_path = os.path.join(
            self.repository_dir, self.RESOURCE_GROUPS_CSV_FILE_NAME
        )
        resource_groups_df = pd.read_csv(resource_groups_csv_path, encoding="utf-8")
        return resource_groups_df

    def _read_resource_group_members_df(self):
        resource_group_members_csv_path = os.path.join(
            self.repository_dir, self.RESOURCE_GROUP_MEMBERS_CSV_FILE_NAME
        )
        resource_group_members_df = pd.read_csv(
            resource_group_members_csv_path, encoding="utf-8"
        )
        return resource_group_members_df

    def _read_jobs_df(self):
        jobs_csv_path = os.path.join(self.repository_dir, self.JOBS_CSV_FILE_NAME)
        jobs_df = pd.read_csv(jobs_csv_path, encoding="utf-8")

        if jobs_df.isna().any().any():
            raise DataIntegrityError("空白のデータが存在します.")

        return jobs_df

    def _read_job_order_constraints_df(self):
        job_order_constraints_csv_path = os.path.join(
            self.repository_dir, self.JOB_ORDER_CONSTRAINTS_CSV_FILE_NAME
        )
        job_order_constraints_df = pd.read_csv(
            job_order_constraints_csv_path, encoding="utf-8"
        )
        return job_order_constraints_df

    def _read_job_required_resource_groups_df(self):
        job_required_resource_groups_csv_path = os.path.join(
            self.repository_dir, self.JOB_REQUIRED_RESOURCE_GROUPS_CSV_FILE_NAME
        )
        job_required_resource_groups_df = pd.read_csv(
            job_required_resource_groups_csv_path, encoding="utf-8"
        )
        return job_required_resource_groups_df

    def _read_operation_assigned_resources_df(self):
        operation_assigned_resources_csv_path = os.path.join(
            self.repository_dir, self.OPERATION_ASSIGNED_RESOURCES_CSV_FILE_NAME
        )
        operatioin_assigned_resources_df = pd.read_csv(
            operation_assigned_resources_csv_path, encoding="utf-8"
        )
        return operatioin_assigned_resources_df

    def _read_operations_df(self):
        operations_csv_path = os.path.join(
            self.repository_dir, self.OPERATIONS_CSV_FILE_NAME
        )
        operations_df = pd.read_csv(operations_csv_path, encoding="utf-8")
        return operations_df
