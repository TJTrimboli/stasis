from typing import Dict, Any, Optional
import json
from stix2 import ThreatActor as StixActor
from core.actor import ThreatActor
from utils.logger import get_logger

logger = get_logger(__name__)

class ExportService:
    """Service for exporting threat actor data in various formats."""

    def __init__(self):
        self.supported_formats = ['json', 'stix', 'csv', 'markdown']

    def export_actor(self, actor: ThreatActor, format: str) -> Optional[str]:
        """
        Export threat actor in specified format.
        
        Args:
            actor: ThreatActor object to export
            format: Export format
            
        Returns:
            Optional[str]: Exported data as string
        """
        try:
            if format.lower() not in self.supported_formats:
                raise ValueError(f"Unsupported format: {format}")

            if format.lower() == 'json':
                return self._export_json(actor)
            elif format.lower() == 'stix':
                return self._export_stix(actor)
            elif format.lower() == 'csv':
                return self._export_csv(actor)
            elif format.lower() == 'markdown':
                return self._export_markdown(actor)

        except Exception as e:
            logger.error(f"Error exporting actor {actor.actor_id}: {str(e)}")
            return None

    def _export_json(self, actor: ThreatActor) -> str:
        """Export actor as JSON string."""
        return json.dumps(actor.to_dict(), indent=2)

    def _export_stix(self, actor: ThreatActor) -> str:
        """Export actor as STIX 2.1 JSON string."""
        try:
            stix_actor = StixActor(
                id=f"threat-actor--{actor.uuid}",
                name=actor.name,
                description=actor.description if hasattr(actor, 'description') else "",
                aliases=actor.aliases,
                first_seen=actor.first_observed,
                last_seen=actor.last_observed,
                sophistication=actor.capability_level,
                resource_level=actor.technical_profile.get('resource_level', 'unknown'),
                primary_motivation=actor.motivation,
                secondary_motivations=actor.strategic_context.get('secondary_motivations', []),
                goals=actor.goals
            )

            return stix_actor.serialize(pretty=True)

        except Exception as e:
            logger.error(f"Error converting to STIX: {str(e)}")
            raise

    def _export_csv(self, actor: ThreatActor) -> str:
        """Export actor as CSV string."""
        try:
            headers = [
                "actor_id", "name", "aliases", "first_observed", "last_observed",
                "confidence_level", "capability_level", "motivation", "goals"
            ]
            
            data = {
                "actor_id": actor.actor_id,
                "name": actor.name,
                "aliases": "|".join(actor.aliases),
                "first_observed": actor.first_observed.isoformat(),
                "last_observed": actor.last_observed.isoformat() if actor.last_observed else "",
                "confidence_level": str(actor.confidence_level),
                "capability_level": actor.capability_level or "",
                "motivation": actor.motivation or "",
                "goals": "|".join(actor.goals)
            }

            # Create CSV string
            csv_lines = [",".join(headers)]
            csv_lines.append(",".join(f'"{data[h]}"' for h in headers))
            return "\n".join(csv_lines)

        except Exception as e:
            logger.error(f"Error converting to CSV: {str(e)}")
            raise

    def _export_markdown(self, actor: ThreatActor) -> str:
        """Export actor as Markdown string."""
        try:
            md_lines = [
                f"# Threat Actor: {actor.name}",
                "",
                f"**ID**: {actor.actor_id}",
                "",
                "## Basic Information",
                f"- **First Observed**: {actor.first_observed.isoformat()}",
                f"- **Last Observed**: {actor.last_observed.isoformat() if actor.last_observed else 'N/A'}",
                f"- **Confidence Level**: {actor.confidence_level}",
                "",
                "### Aliases",
                "- " + "\n- ".join(actor.aliases) if actor.aliases else "- None",
                "",
                "## Technical Profile",
                f"- **Capability Level**: {actor.capability_level or 'Unknown'}",
                "",
                "### Tools and Malware",
                "".join([f"- {tool['name']}: {tool.get('type', 'Unknown')}\n" 
                        for tool in actor.tools_malware]) if actor.tools_malware else "- None documented",
                "",
                "## Behavioral Analysis",
                "### Target Sectors",
                "- " + "\n- ".join(actor.target_sectors) if actor.target_sectors else "- None documented",
                "",
                "### Geographic Targeting",
                "```json",
                json.dumps(actor.geographic_targeting, indent=2),
                "```",
                "",
                "## Strategic Context",
                f"- **Primary Motivation**: {actor.motivation or 'Unknown'}",
                "",
                "### Goals",
                "- " + "\n- ".join(actor.goals) if actor.goals else "- None documented",
                "",
                "## References",
                "".join([f"- [{ref.title}]({ref.url})\n" 
                        for ref in actor.references if ref.url]) if actor.references else "- None"
            ]

            return "\n".join(md_lines)

        except Exception as e:
            logger.error(f"Error converting to Markdown: {str(e)}")
            raise

    def export_multiple_actors(self, actors: list, format: str) -> Optional[str]:
        """
        Export multiple actors in specified format.
        
        Args:
            actors: List of ThreatActor objects
            format: Export format
            
        Returns:
            Optional[str]: Exported data as string
        """
        try:
            if format.lower() == 'json':
                return json.dumps([actor.to_dict() for actor in actors], indent=2)
                
            elif format.lower() == 'stix':
                stix_bundle = {
                    "type": "bundle",
                    "id": f"bundle--{uuid4()}",
                    "objects": [self._export_stix(actor) for actor in actors]
                }
                return json.dumps(stix_bundle, indent=2)
                
            elif format.lower() == 'csv':
                headers = [
                    "actor_id", "name", "aliases", "first_observed", "last_observed",
                    "confidence_level", "capability_level", "motivation", "goals"
                ]
                
                csv_lines = [",".join(headers)]
                for actor in actors:
                    data = {
                        "actor_id": actor.actor_id,
                        "name": actor.name,
                        "aliases": "|".join(actor.aliases),
                        "first_observed": actor.first_observed.isoformat(),
                        "last_observed": actor.last_observed.isoformat() if actor.last_observed else "",
                        "confidence_level": str(actor.confidence_level),
                        "capability_level": actor.capability_level or "",
                        "motivation": actor.motivation or "",
                        "goals": "|".join(actor.goals)
                    }
                    csv_lines.append(",".join(f'"{data[h]}"' for h in headers))
                return "\n".join(csv_lines)
                
            elif format.lower() == 'markdown':
                md_sections = []
                for actor in actors:
                    md_sections.append(self._export_markdown(actor))
                    md_sections.append("\n---\n")
                return "\n".join(md_sections)

        except Exception as e:
            logger.error(f"Error exporting multiple actors: {str(e)}")
            return None

    def export_to_file(self, actor: ThreatActor, format: str, filepath: str) -> bool:
        """
        Export actor to file.
        
        Args:
            actor: ThreatActor object to export
            format: Export format
            filepath: Path to output file
            
        Returns:
            bool: True if export successful
        """
        try:
            content = self.export_actor(actor, format)
            if content is None:
                return False

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        except Exception as e:
            logger.error(f"Error exporting to file {filepath}: {str(e)}")
            return False
