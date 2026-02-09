from typing import Optional, List, Dict
from dataclasses import dataclass, field


@dataclass
class JobInfo:
    # --- 必須フィールド ---
    job_id: int
    name: str
    # --- オプションフィールド（デフォルト値あり） ---
    need_time_buckets: int = 0
    parent_job_id: int = 0  # 親job
    start_time_backet_id: Optional[int] = None

    # --- リストフィールド （初期化時は空）---
    predecessor_job_ids: List[int] = field(default_factory=list, init=False)  # 後job
    required_recource_group_ids: Dict[int, int] = field(
        default_factory=dict, init=False
    )
    assigned_resource_ids: Dict[int, int] = field(default_factory=dict, init=False)
