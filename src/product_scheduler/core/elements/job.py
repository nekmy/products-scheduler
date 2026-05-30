from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Dict, Optional

import numpy as np

if TYPE_CHECKING:
    from product_scheduler.core.elements.resource_group import ResourceGroup
    from product_scheduler.core.elements.operation import Operation


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
    start_time_bucket_id: Optional[int] = None

    # --- リストフィールド （初期化時は空）---
    parents: List["Job"] = field(default_factory=list, init=False)  # 親job
    children: List["Job"] = field(default_factory=list, init=False)  # 子job
    predecessors: List["Job"] = field(default_factory=list, init=False)  # 前job
    successors: List["Job"] = field(default_factory=list, init=False)  # 後job
    required_resource_groups: Dict[ResourceGroup, int] = field(
        default_factory=dict, init=False
    )
    operations: List[Operation] = field(default_factory=list, init=False)  # 順序を持つ

    def __repr__(self):
        return self.name
