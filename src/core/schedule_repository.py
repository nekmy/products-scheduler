import os
import pandas as pd

from core.scheduler import Scheduler
from core.elements.job import Job
from core.elements.resource import Resource


class DataIntegrityError(Exception):
    """データの不整合を表す例外"""

    pass


class ScheduleRepository:
    TIME_BUCKETS_CSV_FILE_NAME = "time_buckets.csv"
    RESOURCES_CSV_FILE_NAME = "recources.csv"
    JOBS_CSV_FILE_NAME = "jobs.csv"
    JOB_ORDER_CONSTRAINTS_CSV_FILE_NAME = "job_order_constraints.csv"

    def __init__(self, repository_dir):
        self.repository_dir = repository_dir

    def read_scheduler(self):
        scheduler = Scheduler()

        resource_kind_map = self._read_resource_kind_map()

        for resource_kind in resource_kind_map.values():
            scheduler.add_resource_kind(resource_kind)

        resource_map = self._read_resource_map(resource_kind_map)

        for resource in resource_map.values():
            scheduler.add_resource(resource)

        job_map = self._read_job_map(scheduler.root_job)
        for job in job_map.values():
            scheduler.add_job(job)

        return scheduler

    def _read_resource_kind_map(self):
        resource_kind_map = {}
        return resource_kind_map

    def _read_resource_map(self):
        resource_map = {}
        resources_df = self._read_resources_df()
        for row in resources_df.itertuples():
            resource = Resource(resource_id=row.resource_id, name=row.name)
            resource_map[resource.resource_id] = resource
        return resource_map

    def _read_job_map(self, root_job: Job):
        jobs_df = self._read_jobs_df()
        job_order_constraints_df = self._read_job_order_constraints_df()
        # rootジョブを加える.
        job_map = {0: root_job}
        job_map |= {
            row.job_id: Job(
                job_id=row.job_id,
                name=row.name,
                need_time_buckets=row.need_time_buckets,
            )
            for row in jobs_df.itertuples()
        }

        for row in jobs_df.itertuples():
            if row.job_id not in job_map:
                raise DataIntegrityError()
            if row.parent_job_id not in job_map:
                raise DataIntegrityError()
            job = job_map[row.job_id]
            parent_job = job_map[row.parent_job_id]
            job.parent = parent_job
            parent_job.children.append(job)

        for row in job_order_constraints_df.itertuples():
            if row.job_id not in job_map:
                raise DataIntegrityError()
            if row.prev_job_id not in job_map:
                raise DataIntegrityError()
            job: Job = job_map[row.job_id]
            prev_job: Job = job_map[row.prev_job_id]
            prev_job.successors.append(job)
            job.predecessors.append(prev_job)

        return job_map

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

    def _read_resources_df(self):
        resources_csv_path = os.path.join(
            self.repository_dir, self.RESOURCES_CSV_FILE_NAME
        )
        resources_df = pd.read_csv(resources_csv_path, encoding="utf-8").set_index(
            "line_id"
        )
        return resources_df
