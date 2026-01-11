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

        for job in self._read_jobs():
            scheduler.add_job(job)

        return scheduler

    def _read_lines(self):
        lines = []
        lines_df = self._read_lines_df()
        for line_info in lines_df.itertuples():
            line = Line(line_info.Index, line_info.line_name)
            lines.append(line)
        return lines

    def _read_jobs(self):
        jobs_df = self._read_jobs_df()
        prev_job_infos_df = self._read_prev_job_infos_df()
        tasks_df = self._read_tasks_df()
        prev_tasks_infos_df = self._read_prev_task_infos_df()
        jobs = []
        for job_info in jobs_df.itertuples():
            job_id = job_info.Index
            prev_job_ids = prev_job_infos_df.loc[
                prev_job_infos_df["job_id"] == job_id, "prev_job_id"
            ].tolist()
            tasks = []
            for task_info in tasks_df.loc[job_id].itertuples():
                job_task_id = task_info.Index
                prev_job_task_ids = prev_tasks_infos_df.loc[
                    (prev_tasks_infos_df["job_id"] == job_id)
                    * (prev_tasks_infos_df["job_task_id"] == job_task_id),
                    "prev_job_task_id",
                ].tolist()
                task = Task(
                    task_id=job_task_id,
                    need_time_buckets=task_info.need_time_buckets,
                    prev_job_task_ids=prev_job_task_ids,
                    start_time_buckets_delta=0,
                )
                tasks.append(task)
            job = Job(
                job_id=job_id,
                name=job_info.name,
                need_time_buckets=job_info.need_time_buckets,
                parent=parent,
                start_time_backet_id=job_info.start_time_bucket_id,
                assigned_line_id=job_info.assigned_line_id,
            )
            jobs.append(job)
        return jobs

    def _read_jobs_df(self):
        jobs_csv_path = os.path.join(self.repository_dir, self.JOBS_CSV_FILE_NAME)
        jobs_df = pd.read_csv(jobs_csv_path, encoding="utf-8").set_index("job_id")
        return jobs_df

    def _read_prev_job_infos_df(self):
        prev_job_infos_csv_path = os.path.join(
            self.repository_dir, self.PREV_JOB_INFOS_CSV_FILE_NAME
        )
        prev_job_infos_df = pd.read_csv(
            prev_job_infos_csv_path, encoding="utf-8"
        ).set_index("prev_job_info_id")
        return prev_job_infos_df

    def _read_tasks_df(self):
        tasks_csv_path = os.path.join(self.repository_dir, self.TASKS_CSV_FILE_NAME)
        tasks_df = pd.read_csv(tasks_csv_path, encoding="utf-8").set_index(
            ["job_id", "job_task_id"]
        )
        return tasks_df

    def _read_prev_task_infos_df(self):
        prev_task_infos_csv_path = os.path.join(
            self.repository_dir, self.PREV_TASK_INFOS_CSV_FILE_NAME
        )
        prev_task_infos_df = pd.read_csv(
            prev_task_infos_csv_path, encoding="utf-8"
        ).set_index("prev_task_info_id")
        return prev_task_infos_df

    def _read_lines_df(self):
        lines_csv_path = os.path.join(self.repository_dir, self.LINES_CSV_FILE_NAME)
        lines_df = pd.read_csv(lines_csv_path, encoding="utf-8").set_index("line_id")
        return lines_df
