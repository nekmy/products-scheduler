from typing import Optional
from dataclasses import dataclass, field

from product_scheduler.core.elements.enums import JobType


@dataclass
class JobInfo:
    # --- 必須フィールド ---
    job_id: int
    name: str
    job_type: JobType

    # --- リストフィールド （初期化時は空）---
    child_job_ids: list[int] = field(default_factory=list, init=False)  # 親job
    predecessor_job_ids: list[int] = field(default_factory=list, init=False)  # 後job
    required_resource_groups: dict[int, int] = field(default_factory=dict, init=False)
