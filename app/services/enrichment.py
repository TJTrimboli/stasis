from typing import Dict, Any, Optional
import requests
from core.actor import ThreatActor
from core.reference import Reference
from utils.logger import get_logger

logger = get_logger(__name__)

class EnrichmentService:
    """Service for enriching threat actor data from external sources."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_keys = config.get('api_keys', {})

    def enrich_actor(self, actor: ThreatActor) -> bool:
        """
        Enrich threat actor with data from external sources.
        
        Args:
            actor: ThreatActor object to enrich
            
        Returns:
            bool: True if enrichment successful
        """
        try:
            # Attempt enrichment from different sources
            mitre_data = self._query_mitre(actor)
            if mitre_data:
                self._update_actor_with_mitre(actor, mitre_data)

            alienvault_data = self._query_alienvault(actor)
            if alienvault_data:
                self._update_actor_with_alienvault(actor, alienvault_data)

            return True
        except Exception as e:
            logger.error(f"Error enriching actor {actor.actor_id}: {str(e)}")
            return False

    def _query_mitre(self, actor: ThreatActor) -> Optional[Dict[str, Any]]:
        """Query MITRE ATT&CK for actor data."""
        try:
            # Implementation for MITRE ATT&CK API query
            url = f"https://api.mitre.org/groups/{actor.name}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error querying MITRE: {str(e)}")
            return None

    def _query_alienvault(self, actor: ThreatActor) -> Optional[Dict[str, Any]]:
        """Query AlienVault OTX for actor data."""
        try:
            # Implementation for AlienVault OTX API query
            headers = {'X-OTX-API-KEY': self.api_keys.get('alienvault')}
            url = f"https://otx.alienvault.com/api/v1/indicators/actor/{actor.name}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error querying AlienVault: {str(e)}")
            return None

    def _update_actor_with_mitre(self, actor: ThreatActor, mitre_data: Dict[str, Any]) -> None:
        """
        Update actor with MITRE ATT&CK data.
        
        Args:
            actor: ThreatActor object to update
            mitre_data: Data from MITRE ATT&CK
        """
        try:
            # Create reference for MITRE data
            reference = Reference(
                source="MITRE ATT&CK",
                url=f"https://attack.mitre.org/groups/{mitre_data.get('id')}",
                title=f"MITRE ATT&CK Group: {mitre_data.get('name')}",
                confidence=4
            )

            # Update techniques
            if 'techniques' in mitre_data:
                for technique in mitre_data['techniques']:
                    if technique not in actor.attack_patterns:
                        actor.attack_patterns.append({
                            'technique_id': technique['id'],
                            'technique_name': technique['name'],
                            'first_observed': actor.first_observed.isoformat()
                        })

            # Update aliases
            if 'aliases' in mitre_data:
                for alias in mitre_data['aliases']:
                    if alias not in actor.aliases:
                        actor.aliases.append(alias)

            actor.add_reference(reference)

        except Exception as e:
            logger.error(f"Error updating actor with MITRE data: {str(e)}")

    def _update_actor_with_alienvault(self, actor: ThreatActor, alienvault_data: Dict[str, Any]) -> None:
        """
        Update actor with AlienVault OTX data.
        
        Args:
            actor: ThreatActor object to update
            alienvault_data: Data from AlienVault OTX
        """
        try:
            # Create reference for AlienVault data
            reference = Reference(
                source="AlienVault OTX",
                url=f"https://otx.alienvault.com/actor/{actor.name}",
                title=f"AlienVault OTX Actor: {actor.name}",
                confidence=3
            )

            # Update IOCs
            if 'indicators' in alienvault_data:
                for ioc in alienvault_data['indicators']:
                    if 'type' in ioc and ioc['type'] == 'domain':
                        if 'infrastructure' not in actor.technical_profile:
                            actor.technical_profile['infrastructure'] = {'domains': []}
                        if ioc['indicator'] not in actor.technical_profile['infrastructure']['domains']:
                            actor.technical_profile['infrastructure']['domains'].append(ioc['indicator'])

            # Update targeting
            if 'targeted_countries' in alienvault_data:
                for country in alienvault_data['targeted_countries']:
                    if country not in actor.geographic_targeting:
                        actor.geographic_targeting[country] = {
                            'first_seen': actor.first_observed.isoformat(),
                            'confidence': 3
                        }

            actor.add_reference(reference)

        except Exception as e:
            logger.error(f"Error updating actor with AlienVault data: {str(e)}")

    def enrich_with_custom_source(self, actor: ThreatActor, source_name: str, 
                                source_config: Dict[str, Any]) -> bool:
        """
        Enrich actor with data from a custom source.
        
        Args:
            actor: ThreatActor object to enrich
            source_name: Name of custom source
            source_config: Configuration for custom source
            
        Returns:
            bool: True if enrichment successful
        """
        try:
            # Validate source configuration
            if not self._validate_source_config(source_config):
                raise ValueError("Invalid source configuration")

            # Make API request to custom source
            headers = {'Authorization': source_config.get('api_key')}
            url = source_config.get('api_url').format(actor_name=actor.name)
            
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Error querying {source_name}: {response.status_code}")
                return False

            data = response.json()
            
            # Create reference for custom source
            reference = Reference(
                source=source_name,
                url=url,
                title=f"{source_name} Data: {actor.name}",
                confidence=source_config.get('confidence', 3)
            )

            # Update actor with custom source data
            self._update_actor_with_custom_data(actor, data, source_config.get('mapping'))
            
            actor.add_reference(reference)
            return True

        except Exception as e:
            logger.error(f"Error enriching actor with {source_name} data: {str(e)}")
            return False

    def _validate_source_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate custom source configuration.
        
        Args:
            config: Source configuration to validate
            
        Returns:
            bool: True if configuration is valid
        """
        required_fields = ['api_url', 'api_key', 'mapping']
        return all(field in config for field in required_fields)

    def _update_actor_with_custom_data(self, actor: ThreatActor, 
                                     data: Dict[str, Any], 
                                     mapping: Dict[str, str]) -> None:
        """
        Update actor with custom source data using field mapping.
        
        Args:
            actor: ThreatActor object to update
            data: Data from custom source
            mapping: Field mapping configuration
        """
        try:
            for source_field, actor_field in mapping.items():
                if source_field in data:
                    field_path = actor_field.split('.')
                    current = actor
                    
                    # Navigate to the correct nested field
                    for i, path in enumerate(field_path):
                        if i == len(field_path) - 1:
                            # Update the field value
                            setattr(current, path, data[source_field])
                        else:
                            current = getattr(current, path)

        except Exception as e:
            logger.error(f"Error updating actor with custom data: {str(e)}")
