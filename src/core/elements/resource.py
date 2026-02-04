from dataclasses import dataclass, field
from typing import List


@dataclass
class ResourceKind:
    resource_kind_id: int
    name: str
    # --- リストフィールド （初期化時は空）---
    resources: List["Resource"] = field(default_factory=list, init=False)


@dataclass
class Resource:
    resource_id: int
    name: str
    resource_kind: ResourceKind
    capacity: int
