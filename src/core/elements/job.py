from dataclasses import dataclass, field

import numpy as np
from typing import List, Dict, Optional

from elements.resource import ResourceKind, Resource


@dataclass
class Job:
    """
    スケジュールの要素単位であるジョブ
    内部にtaskのリストと完了必要ジョブを持つ
    このクラスはあくまで開始タイムバケットを持つ
    """

    # --- 必須フィールド ---
    job_id: int
    name: str
    # --- オプションフィールド（デフォルト値あり） ---
    need_time_buckets: int = 0
    start_time_backet_id: Optional[int] = None
    parent: Optional["Job"] = None  # 親job

    # --- リストフィールド （初期化時は空）---
    children: List["Job"] = field(default_factory=list, init=False)  # 子job
    predecessors: List["Job"] = field(default_factory=list, init=False)  # 前job
    successors: List["Job"] = field(default_factory=list, init=False)  # 後job
    required_recources: Dict["ResourceKind", int] = field(
        default_factory=dict, init=False
    )
    assigned_recources: Dict["Resource", int] = field(default_factory=dict, init=False)

    def __repr__(self):
        return self.name

    @property
    def total_need_time_buckets(self):
        return max(
            self.need_time_buckets,
            *[
                child.start_time_bucket_id + child.total_need_time_buckets
                for child in self.children
            ]
        )

    def get_prev_jobs_matrix(self):
        n_tasks = len(self.children)
        task_ids = [task.task_id for task in self.children]
        prev_tasks_matrix = np.zeros((n_tasks, n_tasks), dtype=bool)
        for task_idx, task in enumerate(self.children):
            for prev_task_id in task.prev_job_task_ids:
                prev_task_idx = task_ids.index(prev_task_id)
                prev_tasks_matrix[task_idx, prev_task_idx] = 1
        return prev_tasks_matrix
