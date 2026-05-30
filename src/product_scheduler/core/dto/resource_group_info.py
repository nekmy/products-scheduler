from dataclasses import dataclass, field
from typing import List


@dataclass
class ResourceGroupInfo:
    # --- 必須フィールド ---
    resource_group_id: int
    name: str
    # --- リストフィールド （初期化時は空）---
    resource_ids: List[int] = field(default_factory=list, init=False)
