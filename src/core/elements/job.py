import numpy as np
from typing import Self, Optional


class Job:
    """
    スケジュールの要素単位であるジョブ
    内部にtaskのリストと完了必要ジョブを持つ
    このクラスはあくまで開始タイムバケットを持つ
    """

    def __init__(
        self,
        job_id: int,
        name: str,
        need_time_buckets: int,
        parent: Optional[Self],  # 親job
        children: list[Self],  # 子job
        predecessors: list[Self],  # 前job
        successors: list[Self],  # 後job
        start_time_backet_id: int,
        assigned_line_id: int,
    ):
        self.job_id = job_id
        self.name = name
        self.need_time_buckets = need_time_buckets

        self.parent = parent
        self.children = children
        self.predecessors = predecessors
        self.successors = successors

        # temp_arrtibutes
        self.start_time_bucket_id = start_time_backet_id
        self.assigned_line_id = assigned_line_id

    @property
    def total_need_time_buckets(self):
        return max(
            self.need_time_buckets,
            *[
                child.start_time_bucket_id + child.total_need_time_buckets
                for child in self.children
            ]
        )

    def get_prev_tasks_matrix(self):
        n_tasks = len(self.children)
        task_ids = [task.task_id for task in self.children]
        prev_tasks_matrix = np.zeros((n_tasks, n_tasks), dtype=bool)
        for task_idx, task in enumerate(self.children):
            for prev_task_id in task.prev_job_task_ids:
                prev_task_idx = task_ids.index(prev_task_id)
                prev_tasks_matrix[task_idx, prev_task_idx] = 1
        return prev_tasks_matrix
