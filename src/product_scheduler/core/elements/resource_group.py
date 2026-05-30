from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Any

if TYPE_CHECKING:
    from .resource import Resource


@dataclass
class ResourceGroup:
    resource_group_id: int
    name: str
    # --- リストフィールド （初期化時は空）---
    resources: List[Resource] = field(default_factory=list, init=False)

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.resource_group_id)

    def __eq__(self, other: Any):
        if not isinstance(other, ResourceGroup):
            return NotImplemented
        return self.resource_group_id == other.resource_group_id
