import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from core.actor import ThreatActor
from core.reference import Reference
from utils.logger import get_logger

logger = get_logger(__name__)

class ActorDatabase:
    """
    Database manager for threat actor data.
    """
    def __init__(self, data_dir: str = None):
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent / 'data'
        self.actors_dir = self.data_dir / 'actors'
        self.references_dir = self.data_dir / 'references'
        
        # Create directories if they don't exist
        self.actors_dir.mkdir(parents=True, exist_ok=True)
        self.references_dir.mkdir(parents=True, exist_ok=True)
        
        self.actors: Dict[str, ThreatActor] = {}
        self._load_actors()

    def _load_actors(self) -> None:
        """Load all threat actors from disk."""
        for actor_file in self.actors_dir.glob('*.json'):
            try:
                with open(actor_file, 'r') as f:
                    actor_data = json.load(f)
                    actor = ThreatActor(**actor_data)
                    self.actors[actor.actor_id] = actor
                    logger.info(f"Loaded actor {actor.actor_id}")
            except Exception as e:
                logger.error(f"Error loading actor from {actor_file}: {str(e)}")

    def save_actor(self, actor: ThreatActor) -> bool:
        """
        Save a threat actor to disk.
        
        Args:
            actor: ThreatActor object to save
            
        Returns:
            bool: True if save successful
        """
        try:
            actor_path = self.actors_dir / f"{actor.actor_id}.json"
            with open(actor_path, 'w') as f:
                json.dump(actor.to_dict(), f, indent=2)
            
            self.actors[actor.actor_id] = actor
            logger.info(f"Saved actor {actor.actor_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving actor {actor.actor_id}: {str(e)}")
            return False

    def get_actor(self, actor_id: str) -> Optional[ThreatActor]:
        """Retrieve a threat actor by ID."""
        return self.actors.get(actor_id)

    def update_actor(self, actor_id: str, field: str, value: any, reference: Reference) -> bool:
        """
        Update a specific field of a threat actor.
        
        Args:
            actor_id: ID of the actor to update
            field: Field name to update
            value: New value
            reference: Reference for the update
            
        Returns:
            bool: True if update successful
        """
        actor = self.get_actor(actor_id)
        if not actor:
            logger.error(f"Actor {actor_id} not found")
            return False

        try:
            actor.update_field(field, value, reference)
            return self.save_actor(actor)
        except Exception as e:
            logger.error(f"Error updating actor {actor_id}: {str(e)}")
            return False

    def search_actors(self, **kwargs) -> List[ThreatActor]:
        """
        Search for actors based on criteria.
        
        Args:
            **kwargs: Search criteria as key-value pairs
            
        Returns:
            List[ThreatActor]: Matching actors
        """
        results = []
        for actor in self.actors.values():
            match = True
            for key, value in kwargs.items():
                if not hasattr(actor, key) or getattr(actor, key) != value:
                    match = False
                    break
            if match:
                results.append(actor)
        return results

    def add_reference(self, actor_id: str, reference: Reference) -> bool:
        """Add a reference to an actor."""
        actor = self.get_actor(actor_id)
        if not actor:
            logger.error(f"Actor {actor_id} not found")
            return False

        try:
            actor.add_reference(reference)
            return self.save_actor(actor)
        except Exception as e:
            logger.error(f"Error adding reference to actor {actor_id}: {str(e)}")
            return False

    def export_actor(self, actor_id: str, format: str = 'json') -> Optional[str]:
        """
        Export an actor in the specified format.
        
        Args:
            actor_id: ID of the actor to export
            format: Export format ('json' or 'stix')
            
        Returns:
            Optional[str]: Exported data as string
        """
        actor = self.get_actor(actor_id)
        if not actor:
            logger.error(f"Actor {actor_id} not found")
            return None

        try:
            if format.lower() == 'json':
                return json.dumps(actor.to_dict(), indent=2)
            elif format.lower() == 'stix':
                from services.export import convert_to_stix
                return convert_to_stix(actor)
            else:
                raise ValueError(f"Unsupported export format: {format}")
        except Exception as e:
            logger.error(f"Error exporting actor {actor_id}: {str(e)}")
            return None
