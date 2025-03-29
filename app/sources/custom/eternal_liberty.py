from typing import Dict, Any, List
import aiohttp
from datetime import datetime
from .source_template import CustomSource
from utils.logger import get_logger

logger = get_logger(__name__)

class EternalLibertySource(CustomSource):
    """Implementation for EternalLiberty threat actor data source."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.url = config['url']
        self.mapping = config['mapping']

    async def fetch_data(self) -> List[Dict[str, Any]]:
        """Fetch data from EternalLiberty GitHub repository."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error fetching data: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching EternalLiberty data: {str(e)}")
            return []

    async def parse_data(self, raw_data: Any) -> List[Dict[str, Any]]:
        """Parse EternalLiberty data into STASIS format."""
        try:
            actors = []
            for raw_actor in raw_data.get('actors', []):
                actor = {
                    'actor_id': f"TA{datetime.now().strftime('%y')}{raw_actor.get('country', 'UNK')}-APT{len(actors):03d}",
                    'name': raw_actor.get('name'),
                    'aliases': raw_actor.get('aliases', []),
                    'first_observed': raw_actor.get('first_seen'),
                    'last_observed': raw_actor.get('last_seen'),
                    'confidence_level': 3,
                    'capability_level': self._map_capability(raw_actor.get('sophistication')),
                    'tools_malware': self._parse_tools(raw_actor.get('tools', [])),
                    'target_sectors': raw_actor.get('targets', []),
                    'geographic_targeting': {
                        'primary_location': raw_actor.get('country'),
                        'target_regions': raw_actor.get('target_regions', [])
                    },
                    'motivation': raw_actor.get('motivation'),
                    'goals': raw_actor.get('objectives', []),
                    'metadata': {
                        'source': 'EternalLiberty',
                        'url': self.url,
                        'version': raw_data.get('version', '1.0.0'),
                        'last_updated': datetime.now().isoformat()
                    }
                }
                actors.append(actor)
            return actors

        except Exception as e:
            logger.error(f"Error parsing EternalLiberty data: {str(e)}")
            return []

    def _map_capability(self, sophistication: str) -> str:
        """Map EternalLiberty sophistication levels to STASIS capability levels."""
        mapping = {
            'low': 'Basic',
            'medium': 'Intermediate',
            'high': 'Advanced'
        }
        return mapping.get(sophistication.lower(), 'Unknown')

    def _parse_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse tools data into standardized format."""
        parsed_tools = []
        for tool in tools:
            parsed_tool = {
                'name': tool.get('name'),
                'type': tool.get('type', 'Unknown'),
                'first_seen': tool.get('first_seen'),
                'description': tool.get('description'),
                'capabilities': tool.get('capabilities', [])
            }
            parsed_tools.append(parsed_tool)
        return parsed_tools

    def validate_data(self, parsed_data: List[Dict[str, Any]]) -> bool:
        """Validate parsed data against STASIS schema."""
        try:
            from core.validation import SchemaValidator
            validator = SchemaValidator()
            
            for actor in parsed_data:
                # Validate core identification
                if not validator.validate_data(
                    {"core_identification": actor}, "identification"
                ):
                    logger.error(f"Invalid identification data for actor: {actor.get('name')}")
                    return False

                # Validate technical profile
                if not validator.validate_data(
                    {"technical_profile": {
                        "capability_level": actor.get('capability_level'),
                        "tools_malware": actor.get('tools_malware', []),
                        "infrastructure": actor.get('infrastructure', {})
                    }}, 
                    "technical"
                ):
                    logger.error(f"Invalid technical data for actor: {actor.get('name')}")
                    return False

                # Validate behavioral analysis
                if not validator.validate_data(
                    {"behavioral_analysis": {
                        "target_sectors": actor.get('target_sectors', []),
                        "geographic_targeting": actor.get('geographic_targeting', {}),
                        "attack_patterns": actor.get('attack_patterns', [])
                    }},
                    "behavioral"
                ):
                    logger.error(f"Invalid behavioral data for actor: {actor.get('name')}")
                    return False

            return True

        except Exception as e:
            logger.error(f"Error validating EternalLiberty data: {str(e)}")
            return False
