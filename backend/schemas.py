from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class FileUpdate:
    name: Optional[str] = None
    path: Optional[str] = None
    comment: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        if not data:
            return cls()
        path = data.get('path')
        if path is None:
            path = data.get('new_path')
        return cls(
            name=data.get('name'),
            path=path,
            comment=data.get('comment'),
        )
