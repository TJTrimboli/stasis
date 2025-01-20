from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from .metadata import Metadata
from .reference import Reference
from .validation import validate_actor_data

@dataclass
class ThreatActor:
    """
    Core threat actor class representing a single threat actor entity.
    """
    actor_id: str
    name: str
    metadata: Metadata
    references: List[Reference] = field(default_factory=list)
    uuid: UUID = field(default_factory=uuid4)
    
    # Core identification
    aliases: List[str] = field(default_factory=list)
    first_observed: datetime = field(default_factory=datetime.now)
    last_observed: Optional[datetime] = None
    confidence_level: int = 0
    
    # Technical profile
    capability_level: Optional[str] = None
    tools_malware: List[Dict] = field(default_factory=list)
    infrastructure: Dict = field(default_factory=dict)
    
    # Behavioral analysis
    target_sectors: List[str] = field(default_factory=list)
    geographic_targeting: Dict = field(default_factory=dict)
    attack_patterns: List[Dict] = field(default_factory=list)
    
    # Strategic context
    motivation: Optional[str] = None
    goals: List[str] = field(default_factory=list)
    relationships: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        """Validate actor data against schema after initialization."""
        validate_actor_data(self.to_dict())

    def add_reference(self, reference: Reference) -> None:
        """Add a new reference with validation."""
        if reference not in self.references:
            self.references.append(reference)
            self._update_metadata()

    def update_field(self, field_name: str, value: any, reference: Reference) -> None:
        """Update a field with proper validation and reference tracking."""
        if hasattr(self, field_name):
            old_value = getattr(self, field_name)
            setattr(self, field_name, value)
            
            try:
                validate_actor_data(self.to_dict())
                self.add_reference(reference)
            except ValueError as e:
                setattr(self, field_name, old_value)
                raise ValueError(f"Invalid update to {field_name}: {str(e)}")
            
            self._update_metadata()
        else:
            raise AttributeError(f"Field {field_name} does not exist")

    def to_dict(self) -> Dict:
        """Convert the threat actor to a dictionary format."""
        return {
            "actor_id": self.actor_id,
            "name": self.name, 
            "metadata": self.metadata.to_dict(),
            "references": [ref.to_dict() for ref in self.references],
            "core_identification": {
                "actor_id": self.actor_id,
                "aliases": self.aliases,
                "first_observed": self.first_observed.isoformat(),
                "last_observed": self.last_observed.isoformat() if self.last_observed else None,
                "confidence_level": self.confidence_level
            },
            "technical_profile": {
                "capability_level": self.capability_level,
                "tools_malware": self.tools_malware,
                "infrastructure": self.infrastructure
            },
            "behavioral_analysis": {
                "target_sectors": self.target_sectors,
                "geographic_targeting": self.geographic_targeting,
                "attack_patterns": self.attack_patterns
            },
            "strategic_context": {
                "motivation": self.motivation,
                "goals": self.goals,
                "relationships": self.relationships
            }
        }

    def _update_metadata(self) -> None:
        """Update metadata when changes are made."""
        self.metadata.modified = datetime.now()
        self.metadata.version_update("minor")

    def validate(self) -> bool:
        """Validate the entire threat actor object."""
        try:
            validate_actor_data(self.to_dict())
            return True
        except ValueError as e:
            raise ValueError(f"Validation failed: {str(e)}")
