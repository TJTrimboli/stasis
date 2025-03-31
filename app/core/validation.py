import json
import jsonschema
from pathlib import Path
from typing import Dict, Any

class SchemaValidator:
    """
    Validator class for checking data against JSON schemas.
    """
    def __init__(self):
        self.schemas = {}
        self._load_schemas()

    def _load_schemas(self) -> None:
        """Load all JSON schemas from the schemas directory."""
        schema_dir = Path(__file__).parent.parent / 'data' / 'schemas'
        for schema_file in schema_dir.glob('**/*.json'):
            with open(schema_file, 'r') as f:
                schema_name = schema_file.stem
                self.schemas[schema_name] = json.load(f)

    def validate_data(self, data: Dict[str, Any], schema_name: str) -> bool:
        """
        Validate data against a specific schema.
        
        Args:
            data: Dictionary containing the data to validate
            schema_name: Name of the schema to validate against
            
        Returns:
            bool: True if validation successful
            
        Raises:
            ValueError: If validation fails
            KeyError: If schema not found
        """
        if schema_name not in self.schemas:
            raise KeyError(f"Schema {schema_name} not found")
            
        try:
            jsonschema.validate(instance=data, schema=self.schemas[schema_name])
            return True
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"Validation error: {str(e)}")

def validate_actor_data(data: Dict[str, Any]) -> bool:
    """
    Validate threat actor data against all relevant schemas.
    """
    validator = SchemaValidator()
    
    # Validate each component
    validator.validate_data(data["core_identification"], "identification")
    validator.validate_data(data["technical_profile"], "technical")
    validator.validate_data(data["behavioral_analysis"], "behavioral")
    validator.validate_data(data["strategic_context"], "strategic")
    validator.validate_data(data["metadata"], "metadata")
    
    return True
