from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

@dataclass
class Reference:
    """
    Reference class for tracking sources and citations.
    """
    source: str
    url: Optional[str] = None
    date: datetime = field(default_factory=datetime.now)
    reference_id: UUID = field(default_factory=uuid4)
    title: Optional[str] = None
    description: Optional[str] = None
    type: str = "external"
    confidence: int = 0
    tags: List[str] = field(default_factory=list)
    fields_referenced: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert reference to dictionary format."""
        return {
            "reference_id": str(self.reference_id),
            "source": self.source,
            "url": self.url,
            "date": self.date.isoformat(),
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "confidence": self.confidence,
            "tags": self.tags,
            "fields_referenced": self.fields_referenced
        }

    def validate(self) -> bool:
        """Validate reference data."""
        if not self.source:
            raise ValueError("Source is required")
        if self.confidence < 0 or self.confidence > 5:
            raise ValueError("Confidence must be between 0 and 5")
        if self.url and not self.url.startswith(('http://', 'https://')):
            raise ValueError("URL must be valid and start with http:// or https://")
        return True
