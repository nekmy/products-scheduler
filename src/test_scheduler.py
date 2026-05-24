from tkinter.filedialog import askdirectory

from core.scheduler import Scheduler
from core.interfaces.schedule_repository import SchedulRepository
from core.elements.job import Job
from core.elements.task import Task


def get_test_scheduler_1():
    scheduler = Scheduler()
    tasks_1 = []
    task_1_1 = Task(need_time_buckets=2, prev_tasks=[], nead_resources={})
    task_1_2 = Task(need_time_buckets=1, prev_tasks=[task_1_1], nead_resources={})
    tasks_1.append(task_1_1)
    tasks_1.append(task_1_2)
    job_1 = Job(tasks=tasks_1, prev_job_ids=[])
    scheduler.load_jobs(job_1)
    return scheduler


def get_test_scheduler_2():
    scheduler = Scheduler()
    # repository = JobRepository(repository_dir=askdirectory())
    repository = SchedulRepository(repository_dir="..\\datas\\datas_sample_20260103_00")

    jobs: list[Job] = repository._read_jobs()
    for job in jobs:
        scheduler.load_jobs(job)
    return scheduler


def main():
    scheduler = get_test_scheduler_2()
    pass


if __name__ == "__main__":
    main()
