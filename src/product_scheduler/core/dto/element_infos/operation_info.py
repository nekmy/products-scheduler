from typing import Optional, Dict
from dataclasses import dataclass, field


@dataclass
class OperationInfo:
    # --- 必須フィールド ---
    operation_id: int
    name: str
    parent_id: int
    sequence_index: int  # job内の実施順序

    # --- オプションフィールド（デフォルト値あり） ---
    job_id: Optional[int] = None

    # --- リストフィールド（初期化時は空） ---
    assigned_amount_of_resource_ids: Dict[int, int] = field(
        default_factory=dict, init=False
    )
