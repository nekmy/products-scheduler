from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Any

if TYPE_CHECKING:
    from product_scheduler.core.elements.resource_group import ResourceGroup


@dataclass
class Resource:
    resource_id: int
    name: str
    capacity: int
    resource_groups: List[ResourceGroup] = field(default_factory=list, init=False)

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.resource_id)

    def __eq__(self, other: Any):
        if not isinstance(other, Resource):
            return NotImplemented
        return self.resource_id == other.resource_id
