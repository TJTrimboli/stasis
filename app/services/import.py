from typing import Dict, Any, Optional, List
import json
import csv
from pathlib import Path
from datetime import datetime
from core.actor import ThreatActor
from core.metadata import Metadata
from core.reference import Reference
from utils.logger import get_logger
from utils.helpers import sanitize_data

logger = get_logger(__name__)

class ImportService:
    """Service for importing threat actor data from various sources."""

    def __init__(self):
        self.supported_formats = ['json', 'stix', 'csv']

    def import_actor(self, data: Any, format: str) -> Optional[ThreatActor]:
        """
        Import threat actor from data in specified format.
        
        Args:
            data: Input data
            format: Input format
            
        Returns:
            Optional[ThreatActor]: Imported actor object
        """
        try:
            if format.lower() not in self.supported_formats:
                raise ValueError(f"Unsupported format: {format}")

            if format.lower() == 'json':
                return self._import_json(data)
            elif format.lower() == 'stix':
                return self._import_stix(data)
            elif format.lower() == 'csv':
                return self._import_csv(data)

        except Exception as e:
            logger.error(f"Error importing actor: {str(e)}")
            return None

    def _import_json(self, data: Dict[str, Any]) -> ThreatActor:
        """Import actor from JSON data."""
        try:
            # Sanitize input data
            data = sanitize_data(data)

            # Create metadata
            metadata = Metadata(
                created=datetime.now(),
                modified=datetime.now(),
                version="1.0.0",
                creator="ImportService"
            )

            # Create references
            references = []
            if 'references' in data:
                for ref_data in data['references']:
                    references.append(Reference(**ref_data))

            # Create actor object
            actor_data = {
                'actor_id': data['actor_id'],
                'name': data['name'],
                'metadata': metadata,
                'references': references
            }

            # Add optional fields if present
            optional_fields = [
                'aliases', 'first_observed', 'last_observed', 'confidence_level',
                'capability_level', 'tools_malware', 'infrastructure',
                'target_sectors', 'geographic_targeting', 'attack_patterns',
                'motivation', 'goals', 'relationships'
            ]

            for field in optional_fields:
                if field in data:
                    actor_data[field] = data[field]

            return ThreatActor(**actor_data)

        except Exception as e:
            logger.error(f"Error importing JSON data: {str(e)}")
            raise

    def _import_stix(self, data: Dict[str, Any]) -> ThreatActor:
        """Import actor from STIX data."""
        try:
            # Convert STIX format to internal format
            actor_data = {
                'actor_id': data['id'].split('--')[1],
                'name': data['name'],
                'aliases': data.get('aliases', []),
                'first_observed': datetime.fromisoformat(data['first_seen'].replace('Z', '+00:00')),
                'last_observed': datetime.fromisoformat(data['last_seen'].replace('Z', '+00:00')) if 'last_seen' in data else None,
                'confidence_level': 3,  # Default confidence level
                'capability_level': data.get('sophistication', 'Unknown'),
                'motivation': data.get('primary_motivation', 'Unknown'),
                'goals': data.get('goals', [])
            }

            # Create metadata
            metadata = Metadata(
                created=datetime.now(),
                modified=datetime.now(),
                version="1.0.0",
                creator="ImportService",
                tlp_level="AMBER"  # Default TLP level
            )

            # Create reference for STIX source
            reference = Reference(
                source="STIX Import",
                title=f"STIX Data: {actor_data['name']}",
                confidence=3
            )

            actor_data['metadata'] = metadata
            actor_data['references'] = [reference]

            return ThreatActor(**actor_data)

        except Exception as e:
            logger.error(f"Error importing STIX data: {str(e)}")
            raise

    def _import_csv(self, data: str) -> ThreatActor:
        """Import actor from CSV data."""
        try:
            # Parse CSV data
            csv_reader = csv.DictReader(data.splitlines())
            row = next(csv_reader)  # Assume single actor per CSV

            actor_data = {
                'actor_id': row['actor_id'],
                'name': row['name'],
                'aliases': row['aliases'].split('|') if row['aliases'] else [],
                'first_observed': datetime.fromisoformat(row['first_observed']),
                'last_observed': datetime.fromisoformat(row['last_observed']) if row['last_observed'] else None,
                'confidence_level': int(row['confidence_level']),
                'capability_level': row['capability_level'] or None,
                'motivation': row['motivation'] or None,
                'goals': row['goals'].split('|') if row['goals'] else []
            }

            # Create metadata
            metadata = Metadata(
                created=datetime.now(),
                modified=datetime.now(),
                version="1.0.0",
                creator="ImportService"
            )

            # Create reference for CSV source
            reference = Reference(
                source="CSV Import",
                title=f"CSV Data: {actor_data['name']}",
                confidence=3
            )

            actor_data['metadata'] = metadata
            actor_data['references'] = [reference]

            return ThreatActor(**actor_data)

        except Exception as e:
            logger.error(f"Error importing CSV data: {str(e)}")
            raise

    def import_from_file(self, filepath: str) -> Optional[ThreatActor]:
        """
        Import actor from file.
        
        Args:
            filepath: Path to input file
            
        Returns:
            Optional[ThreatActor]: Imported actor object
        """
        try:
            file_path = Path(filepath)
            format = file_path.suffix[1:].lower()  # Remove leading dot

            if format not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {format}")

            with open(filepath, 'r', encoding='utf-8') as f:
                if format == 'json':
                    data = json.load(f)
                elif format == 'csv':
                    data = f.read()
                else:  # STIX
                    data = json.load(f)

            return self.import_actor(data, format)

        except Exception as e:
            logger.error(f"Error importing from file {filepath}: {str(e)}")
            return None

    def import_multiple_files(self, directory: str, format: str = None) -> List[ThreatActor]:
        """
        Import multiple actors from files in directory.
        
        Args:
            directory: Directory containing input files
            format: Optional format override (default: detect from file extension)
            
        Returns:
            List[ThreatActor]: List of imported actor objects
        """
        try:
            dir_path = Path(directory)
            if not dir_path.is_dir():
                raise ValueError(f"Not a directory: {directory}")

            actors = []
            for file_path in dir_path.glob('*.*'):
                if format:
                    file_format = format
                else:
                    file_format = file_path.suffix[1:].lower()

                if file_format in self.supported_formats:
                    actor = self.import_from_file(str(file_path))
                    if actor:
                        actors.append(actor)
                        logger.info(f"Successfully imported actor from {file_path}")
                    else:
                        logger.warning(f"Failed to import actor from {file_path}")

            return actors

        except Exception as e:
            logger.error(f"Error importing from directory {directory}: {str(e)}")
            return []

    def validate_import_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate import data before processing.
        
        Args:
            data: Data to validate
            
        Returns:
            bool: True if data is valid
        """
        try:
            required_fields = ['actor_id', 'name']
            if not all(field in data for field in required_fields):
                return False

            # Validate actor_id format
            if not data['actor_id'].startswith('TA'):
                return False

            # Validate dates if present
            if 'first_observed' in data:
                try:
                    datetime.fromisoformat(data['first_observed'].replace('Z', '+00:00'))
                except ValueError:
                    return False

            if 'last_observed' in data:
                try:
                    datetime.fromisoformat(data['last_observed'].replace('Z', '+00:00'))
                except ValueError:
                    return False

            # Validate confidence level if present
            if 'confidence_level' in data:
                try:
                    conf_level = int(data['confidence_level'])
                    if conf_level < 1 or conf_level > 5:
                        return False
                except ValueError:
                    return False

            return True

        except Exception as e:
            logger.error(f"Error validating import data: {str(e)}")
            return False

    def merge_actor_data(self, existing: ThreatActor, new_data: Dict[str, Any]) -> ThreatActor:
        """
        Merge new data into existing actor.
        
        Args:
            existing: Existing ThreatActor object
            new_data: New data to merge
            
        Returns:
            ThreatActor: Updated actor object
        """
        try:
            # Create reference for merge
            reference = Reference(
                source="Data Merge",
                title=f"Merged Data: {existing.name}",
                confidence=3,
                date=datetime.now()
            )

            # Merge lists
            for field in ['aliases', 'tools_malware', 'target_sectors', 'goals']:
                if field in new_data:
                    existing_list = getattr(existing, field)
                    new_list = new_data[field]
                    merged_list = list(set(existing_list + new_list))
                    setattr(existing, field, merged_list)

            # Update scalar fields if new data has higher confidence
            scalar_fields = ['capability_level', 'motivation']
            for field in scalar_fields:
                if field in new_data and new_data.get('confidence_level', 0) > existing.confidence_level:
                    setattr(existing, field, new_data[field])

            # Merge dictionaries
            dict_fields = ['infrastructure', 'geographic_targeting']
            for field in dict_fields:
                if field in new_data:
                    existing_dict = getattr(existing, field)
                    new_dict = new_data[field]
                    merged_dict = {**existing_dict, **new_dict}  # Prefer new values in case of conflict
                    setattr(existing, field, merged_dict)

            # Update timestamps
            if 'last_observed' in new_data:
                new_last_observed = datetime.fromisoformat(new_data['last_observed'].replace('Z', '+00:00'))
                if not existing.last_observed or new_last_observed > existing.last_observed:
                    existing.last_observed = new_last_observed

            # Add reference for the merge
            existing.add_reference(reference)

            # Update metadata
            existing.metadata.modified = datetime.now()
            existing.metadata.version_update("minor")

            return existing

        except Exception as e:
            logger.error(f"Error merging actor data: {str(e)}")
            raise

    def import_relationships(self, actor: ThreatActor, relationship_data: List[Dict[str, Any]]) -> bool:
        """
        Import relationship data for an actor.
        
        Args:
            actor: ThreatActor object to update
            relationship_data: List of relationship dictionaries
            
        Returns:
            bool: True if import successful
        """
        try:
            for relationship in relationship_data:
                if not self._validate_relationship(relationship):
                    logger.warning(f"Invalid relationship data: {relationship}")
                    continue

                # Create reference for relationship
                reference = Reference(
                    source=relationship.get('source', 'Relationship Import'),
                    title=f"Relationship: {actor.name} -> {relationship['related_actor']}",
                    confidence=relationship.get('confidence', 3),
                    date=datetime.now()
                )

                # Add relationship to actor
                new_relationship = {
                    'related_actor': relationship['related_actor'],
                    'relationship_type': relationship['relationship_type'],
                    'first_observed': relationship.get('first_observed', actor.first_observed.isoformat()),
                    'last_observed': relationship.get('last_observed'),
                    'confidence': relationship.get('confidence', 3),
                    'description': relationship.get('description')
                }

                actor.relationships.append(new_relationship)
                actor.add_reference(reference)

            return True

        except Exception as e:
            logger.error(f"Error importing relationships: {str(e)}")
            return False

    def _validate_relationship(self, relationship: Dict[str, Any]) -> bool:
        """
        Validate relationship data.
        
        Args:
            relationship: Relationship dictionary to validate
            
        Returns:
            bool: True if relationship is valid
        """
        required_fields = ['related_actor', 'relationship_type']
        if not all(field in relationship for field in required_fields):
            return False

        valid_types = [
            'Collaborates With',
            'Competes With',
            'Provides Support To',
            'Shares Infrastructure With',
            'Related To'
        ]

        if relationship['relationship_type'] not in valid_types:
            return False

        if 'confidence' in relationship:
            try:
                conf_level = int(relationship['confidence'])
                if conf_level < 1 or conf_level > 5:
                    return False
            except ValueError:
                return False

        return True
