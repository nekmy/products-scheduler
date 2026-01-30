import os
import pandas as pd

from core.scheduler import Scheduler
from core.elements.job import Job
from core.elements.line import Line


class ScheduleRepository:
    TIME_BUCKETS_CSV_FILE_NAME = "time_buckets.csv"
    LINES_CSV_FILE_NAME = "lines.csv"
    JOBS_CSV_FILE_NAME = "jobs.csv"
    PREV_JOB_INFOS_CSV_FILE_NAME = "prev_job_infos.csv"
    TASKS_CSV_FILE_NAME = "tasks.csv"
    PREV_TASK_INFOS_CSV_FILE_NAME = "prev_task_infos.csv"

    def __init__(self, repository_dir):
        self.repository_dir = repository_dir

    def read_scheduler(self):
        scheduler = Scheduler()

        for line in self._read_lines():
            scheduler.add_line(line)

        for job in self._read_job_map():
            scheduler.add_job(job)

        return scheduler

    def _read_lines(self):
        lines = []
        lines_df = self._read_lines_df()
        for line_info in lines_df.itertuples():
            line = Line(line_info.Index, line_info.line_name)
            lines.append(line)
        return lines

    def _read_job_map(self):
        jobs_df = self._read_jobs_df()
        prev_job_infos_df = self._read_prev_job_infos_df()
        job_map = {
            row.job_id: Job(
                job_id=row.job_id,
                name=row.name,
                need_time_buckets=row.need_time_buckets,
            )
            for row in jobs_df.itertuples()
        }
        job_map[0] = Job(job_id=0, name="root")

        for row in jobs_df.itertuples():
            job = job_map[row.job_id]
            parent_job = job_map[row.parent_job_id]
            job.parent = parent_job
            parent_job.children.append(job)

        for row in prev_job_infos_df.itertuples():
            job_id = row.job_id
            prev_job_id = row.prev_job_id
            job: Job = job_map[job_id]
            prev_job: Job = job_map[prev_job_id]
            prev_job.successors.append(job)
            job.predecessors.append(prev_job)

        return job_map

    def _read_jobs_df(self):
        jobs_csv_path = os.path.join(self.repository_dir, self.JOBS_CSV_FILE_NAME)
        jobs_df = pd.read_csv(jobs_csv_path, encoding="utf-8")
        return jobs_df

    def _read_prev_job_infos_df(self):
        prev_job_infos_csv_path = os.path.join(
            self.repository_dir, self.PREV_JOB_INFOS_CSV_FILE_NAME
        )
        prev_job_infos_df = pd.read_csv(prev_job_infos_csv_path, encoding="utf-8")
        return prev_job_infos_df

    def _read_lines_df(self):
        lines_csv_path = os.path.join(self.repository_dir, self.LINES_CSV_FILE_NAME)
        lines_df = pd.read_csv(lines_csv_path, encoding="utf-8").set_index("line_id")
        return lines_df
