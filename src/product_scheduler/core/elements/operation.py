from __future__ import annotations

from typing import List, Dict, Optional, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from product_scheduler.core.elements.job import Job
    from product_scheduler.core.elements.resource import Resource


@dataclass
class Operation:
    """
    実際のスケジュールを示すクラス
    分割を表現することを可能にする.
    """

    # --- 必須フィールド ---
    operation_id: int
    name: str
    # 自身が所属するJob
    job: Job
    # job内で何番目のoperationか
    sequence_index: int

    # --- オプションフィールド（デフォルト値あり） ---
    # 自身が所属する親operation（自身の所属するjobの親jobのoperationのいずれか）jobがroot以外のoperationでは必須
    parent: Optional["Operation"] = None

    # --- リストフィールド（初期化時は空）---
    # 子jobのoperationのうち自身に所属するもの
    children: List["Operation"] = field(default_factory=list, init=False)
    # 割り当てられたリソース
    assigned_resources: Dict[Resource, int] = field(default_factory=dict, init=False)
