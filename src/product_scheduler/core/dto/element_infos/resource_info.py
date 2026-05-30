from dataclasses import dataclass


@dataclass
class ResourceInfo:
    # --- 必須フィールド ---
    resource_id: int
    name: str
    capacity: int
