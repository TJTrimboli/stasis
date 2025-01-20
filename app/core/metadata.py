from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

@dataclass
class Metadata:
    """
    Metadata class for tracking changes and versioning.
    """
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    creator: str = field(default="STASIS")
    tlp_level: str = field(default="AMBER")
    confidence_score: int = field(default=0)
    revision_history: List[Dict] = field(default_factory=list)

    def version_update(self, update_type: str) -> None:
        """
        Update version number based on semantic versioning.
        """
        major, minor, patch = map(int, self.version.split('.'))
        
        if update_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif update_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
            
        self.version = f"{major}.{minor}.{patch}"
        
        self.revision_history.append({
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "type": update_type
        })

    def to_dict(self) -> Dict:
        """Convert metadata to dictionary format."""
        return {
            "created": self.created.isoformat(),
            "modified": self.modified.isoformat(),
            "version": self.version,
            "creator": self.creator,
            "tlp_level": self.tlp_level,
            "confidence_score": self.confidence_score,
            "revision_history": self.revision_history
        }
