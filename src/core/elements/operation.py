from __future__ import annotations

from typing import List, Dict, Optional, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from core.elements.job import Job
    from core.elements.resource import Resource


@dataclass
class Operation:
    """
    実際のスケジュールを示すクラス
    分割を表現することを可能にする.
    """

    # --- 必須フィールド ---
    operation_id: int
    name: str
    sequence_num: int

    # --- オプションフィールド（デフォルト値あり） ---
    # 自身が所属するJob
    job: Optional[Job] = None
    # 自身が所属する親operation（自身の所属するjobの親jobのoperationのいずれか）
    parent: Optional["Operation"] = None

    # --- リストフィールド（初期化時は空）---
    # 子jobのoperationのうち自身に所属するもの
    children: List["Operation"] = field(default_factory=list, init=False)
    # jobに属さないoperation特有の開始operation
    setup_operations: List["Operation"] = field(default_factory=list, init=False)
    # jobに属さないoperation特有の終了operation
    teardown_operations: List["Operation"] = field(default_factory=list, init=False)
    # 割り当てられたリソース
    assigned_resources: Dict[Resource, int] = field(default_factory=dict, init=False)
