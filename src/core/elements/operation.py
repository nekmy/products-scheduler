from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from core.elements.job import Job


@dataclass
class Operation:
    operation_id: int
    parent_op: Operation

    job: Operation[Job] = None
    child_options: List[Operation] = field(default_factory=list)
