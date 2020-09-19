from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class NewsContent:
    title: str
    url: str
    timestamp: Optional[datetime] = None
