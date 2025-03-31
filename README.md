# STASIS (Structured Threat Actor Schema & Intelligence System)

## Overview
STASIS is a comprehensive framework for collecting, managing, and analyzing threat actor information. It provides a standardized approach to threat actor profiling while maintaining flexibility for various intelligence sources and use cases.

## Features
- Standardized threat actor data schema
- Multiple data source support (MITRE ATT&CK, AlienVault OTX, custom sources)
- Flexible storage options (file-based, MongoDB, PostgreSQL)
- Data validation and quality control
- Export capabilities (JSON, STIX 2.1, CSV, Markdown)
- Custom source integration framework
- Comprehensive documentation

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Virtual environment (recommended)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/your-org/stasis.git
cd stasis
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Basic Usage
```python
from stasis import ThreatActorManager

# Initialize manager
manager = ThreatActorManager()

# Create new threat actor
actor = manager.create_actor(
    name="APT123",
    country_code="CHN",
    category="APT"
)

# Add data with reference
manager.update_actor(
    actor_id=actor.actor_id,
    field="capability_level",
    value="Advanced",
    reference={
        "source": "Security Vendor Report",
        "url": "https://example.com/report",
        "title": "APT123 Technical Analysis",
        "date": "2023-12-01"
    }
)

# Export actor data
json_data = manager.export_actor(actor.actor_id, format="json")
```

### Adding Custom Sources

1. Create a new source class in `sources/custom/`:
```python
from sources.custom.source_template import CustomSource

class MyCustomSource(CustomSource):
    def __init__(self, config):
        super().__init__(config)
        # Initialize source-specific configuration
        
    async def fetch_data(self):
        # Implement data fetching logic
        
    async def parse_data(self, raw_data):
        # Implement data parsing logic
        
    def validate_data(self, parsed_data):
        # Implement validation logic
```

2. Add source configuration to `config/config.yaml`:
```yaml
custom_sources:
  my_custom_source:
    enabled: true
    url: https://api.example.com/threat-actors
    api_key: ${MY_SOURCE_API_KEY}
    update_interval: 86400
    confidence: 3
    mapping:
      name: actor_name
      country: origin_country
      # Add field mappings
```

### Configuration

The application can be configured through `config/config.yaml` and environment variables:

#### Database Configuration
```yaml
database:
  type: mongodb  # or postgresql, file
  host: localhost
  port: 27017
  name: stasis
  user: ${DB_USER}
  password: ${DB_PASSWORD}
```

#### Source Configuration
```yaml
sources:
  mitre:
    enabled: true
    url: https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json
    update_interval: 86400

  custom_source:
    enabled: true
    url: https://api.example.com/actors
    api_key: ${SOURCE_API_KEY}
    mapping:
      # Field mappings
```

## Adding New Sources

### Step 1: Create Source Class
Create a new Python file in `sources/custom/` implementing the CustomSource interface.

### Step 2: Configure Mapping
Define field mappings in `config/config.yaml` to translate source-specific fields to STASIS schema.

### Step 3: Implement Validation
Add source-specific validation rules in the source class.

### Step 4: Test Integration
Use the provided test framework to verify source integration:
```bash
pytest tests/sources/test_custom_source.py
```

## Data Model

### Core Components
- Identification
- Technical Profile
- Behavioral Analysis
- Strategic Context
- Metadata

### References
All data points must include references:
```python
reference = {
    "source": "Source Name",
    "url": "https://example.com",
    "title": "Reference Title",
    "date": "2023-12-01",
    "confidence": 4
}
```

## Development

### Setting Up Development Environment
1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Set up pre-commit hooks:
```bash
pre-commit install
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=stasis

# Run specific test category
pytest tests/core/
```

### Code Style
The project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run all checks:
```bash
# Format code
black .

# Sort imports
isort .

# Run linter
flake8 .

# Run type checker
mypy .
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and style checks
5. Submit a pull request

## Production Deployment

### Docker Deployment
```dockerfile
# Dockerfile provided in repository
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-m", "stasis"]
```

Build and run:
```bash
docker build -t stasis .
docker run -d --name stasis -p 8000:8000 stasis
```

### Database Configuration

#### MongoDB
```yaml
database:
  type: mongodb
  host: mongodb.example.com
  port: 27017
  name: stasis
  user: ${MONGO_USER}
  password: ${MONGO_PASSWORD}
  ssl: true
  replica_set: rs0
```

#### PostgreSQL
```yaml
database:
  type: postgresql
  host: postgresql.example.com
  port: 5432
  name: stasis
  user: ${POSTGRES_USER}
  password: ${POSTGRES_PASSWORD}
  ssl_mode: verify-full
  max_connections: 20
```

### Scaling Considerations

1. **Data Volume**
   - Implement data partitioning
   - Set up archival process
   - Configure caching

2. **Performance**
   - Use connection pooling
   - Implement request rate limiting
   - Cache frequently accessed data

3. **High Availability**
   - Deploy multiple instances
   - Set up load balancing
   - Configure database replication

### Monitoring

1. **Application Metrics**
```yaml
monitoring:
  enabled: true
  prometheus_endpoint: /metrics
  statsd:
    host: statsd.example.com
    port: 8125
  custom_metrics:
    - actor_updates
    - source_fetches
    - api_requests
```

2. **Logging**
```yaml
logging:
  level: INFO
  format: json
  outputs:
    - type: file
      path: /var/log/stasis/app.log
    - type: elasticsearch
      host: elasticsearch.example.com
      index: stasis-logs
```

### Backup and Recovery

1. **Database Backups**
```yaml
backup:
  schedule: "0 2 * * *"  # Daily at 2 AM
  retention_days: 30
  storage:
    type: s3
    bucket: stasis-backups
    path: /database
```

2. **Data Export**
```bash
# Export all actors
python -m stasis.tools.export --format json --output /backup/actors.json

# Export specific timeframe
python -m stasis.tools.export --start-date 2023-01-01 --end-date 2023-12-31
```

## API Documentation

### REST API
The application provides a RESTful API for integration:

```bash
# Get actor by ID
GET /api/v1/actors/{actor_id}

# Create new actor
POST /api/v1/actors

# Update actor
PUT /api/v1/actors/{actor_id}

# Search actors
GET /api/v1/actors/search?field=value
```

### GraphQL API
```graphql
query {
  actor(id: "TA23CHN-APT001") {
    name
    aliases
    technical_profile {
      capability_level
      tools_malware {
        name
        type
      }
    }
  }
}
```

## Support

### Community
- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share ideas
- Wiki: Additional documentation and guides

### Commercial Support
For enterprise support options, contact: support@stasis-project.org

## License
Apache License 2.0

## Acknowledgments
- MITRE ATT&CK®
- STIX™
- Community Contributors

## Roadmap

### Version 1.1.0 (TBD)
- Enhanced machine learning integration for actor correlation
- Automated relationship mapping
- Advanced visualization capabilities
- Real-time threat actor tracking
- Improved data enrichment pipeline

### Version 1.2.0 (TBD)
- Advanced analytics dashboard
- Automated report generation
- Enhanced API capabilities
- Additional data source integrations
- Improved search functionality

### Version 2.0.0 (TBD)
- Real-time collaboration features
- Advanced workflow automation
- Machine learning-based prediction
- Enhanced visualization tools
- Extended API capabilities

## Project Structure
```
stasis/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── config.yaml
│   └── logging.yaml
├── core/
│   ├── __init__.py
│   ├── actor.py
│   ├── metadata.py
│   ├── reference.py
│   └── validation.py
├── data/
│   ├── actors/
│   ├── references/
│   └── schemas/
├── services/
│   ├── __init__.py
│   ├── enrichment.py
│   ├── export.py
│   └── import.py
├── sources/
│   ├── __init__.py
│   ├── mitre/
│   ├── alienvault/
│   └── custom/
├── utils/
│   ├── __init__.py
│   ├── database.py
│   ├── logger.py
│   └── helpers.py
├── api/
│   ├── __init__.py
│   ├── rest/
│   └── graphql/
├── ui/
│   ├── __init__.py
│   ├── dashboard/
│   └── components/
├── tests/
│   ├── __init__.py
│   ├── core/
│   ├── services/
│   └── sources/
├── docs/
│   ├── api/
│   ├── deployment/
│   └── development/
├── tools/
│   ├── export.py
│   ├── import.py
│   └── maintenance.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Quick Start Guide

### 1. Installation
```bash
# Clone repository
git clone https://github.com/your-org/stasis.git
cd stasis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml

# Set environment variables
cp .env.example .env
# Edit .env with your settings
```

### 3. Initialize Database
```bash
# Using provided script
python tools/initialize_db.py

# Or using management command
python -m stasis.manage init-db
```

### 4. Import Initial Data
```bash
# Import from MITRE ATT&CK
python tools/import.py --source mitre

# Import from custom source
python tools/import.py --source custom --file path/to/data.json
```

### 5. Start Application
```bash
# Development server
python -m stasis.manage runserver

# Production deployment
docker-compose up -d
```

## Common Tasks

### Adding a New Threat Actor
```python
from stasis import ThreatActorManager

manager = ThreatActorManager()

# Create new actor
actor = manager.create_actor(
    name="APT123",
    country_code="CHN",
    category="APT",
    reference={
        "source": "Internal Analysis",
        "title": "Initial Actor Profile",
        "confidence": 3
    }
)

# Add technical details
manager.update_actor(
    actor_id=actor.actor_id,
    updates={
        "technical_profile": {
            "capability_level": "Advanced",
            "tools_malware": [
                {
                    "name": "CustomRAT",
                    "type": "RAT",
                    "first_seen": "2023-12-01"
                }
            ]
        }
    },
    reference={
        "source": "Technical Analysis Report",
        "url": "https://example.com/analysis",
        "title": "APT123 Technical Capabilities",
        "confidence": 4
    }
)
```

### Importing from Custom Sources

1. Create Source Configuration:
```yaml
# config/sources/custom_source.yaml
name: CustomSource
enabled: true
url: https://api.example.com/threat-actors
api_key: ${CUSTOM_SOURCE_API_KEY}
update_interval: 86400
confidence: 3

mapping:
  name: actor_name
  country: origin_country
  capability: technical_capability
  tools: malware_list
  targets: target_sectors
```

2. Implement Source Handler:
```python
# sources/custom/custom_source.py
from sources.base import BaseSource

class CustomSourceHandler(BaseSource):
    async def fetch_data(self):
        # Implement data fetching
        pass

    async def parse_data(self, raw_data):
        # Implement data parsing
        pass

    def validate_data(self, parsed_data):
        # Implement validation
        pass
```

3. Register and Use Source:
```python
from stasis import SourceManager

# Register source
source_manager = SourceManager()
source_manager.register_source('custom_source', CustomSourceHandler)

# Update from source
await source_manager.update_from_source('custom_source')
```

### Data Export and Reporting

1. Export to Various Formats:
```python
from stasis import ExportManager

export_manager = ExportManager()

# Export to JSON
json_data = export_manager.export_actor(
    actor_id="TA23CHN-APT001",
    format="json"
)

# Export to STIX
stix_data = export_manager.export_actor(
    actor_id="TA23CHN-APT001",
    format="stix"
)

# Export to Markdown report
markdown_report = export_manager.export_actor(
    actor_id="TA23CHN-APT001",
    format="markdown",
    template="detailed_report"
)
```

2. Generate Reports:
```python
from stasis.reporting import ReportGenerator

generator = ReportGenerator()

# Generate comprehensive report
report = generator.generate_report(
    actor_id="TA23CHN-APT001",
    report_type="comprehensive",
    include_sections=[
        "technical_analysis",
        "behavioral_patterns",
        "strategic_assessment"
    ]
)

# Export report
generator.export_report(
    report,
    format="pdf",
    output_path="reports/TA23CHN-APT001_analysis.pdf"
)
```

### Data Maintenance

1. Regular Updates:
```python
from stasis import MaintenanceManager

maintenance = MaintenanceManager()

# Update all sources
await maintenance.update_all_sources()

# Validate data integrity
await maintenance.validate_data()

# Clean up old data
await maintenance.cleanup_old_data(
    older_than_days=90,
    backup=True
)
```

2. Data Validation:
```python
from stasis import ValidationManager

validator = ValidationManager()

# Validate specific actor
validation_result = validator.validate_actor("TA23CHN-APT001")

# Validate all actors
validation_results = validator.validate_all_actors()

# Generate validation report
validator.generate_validation_report(
    output_path="reports/validation_report.pdf"
)
```

### API Usage Examples

1. REST API:
```python
import requests

# Configuration
API_BASE = "https://api.stasis.org/v1"
API_KEY = "your-api-key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Get actor details
response = requests.get(
    f"{API_BASE}/actors/TA23CHN-APT001",
    headers=headers
)
actor_data = response.json()

# Search actors
response = requests.get(
    f"{API_BASE}/actors/search",
    params={
        "capability_level": "Advanced",
        "target_sector": "Technology"
    },
    headers=headers
)
search_results = response.json()

# Create new actor
new_actor = {
    "name": "APT123",
    "country_code": "CHN",
    "category": "APT",
    "reference": {
        "source": "Internal Analysis",
        "confidence": 3
    }
}

response = requests.post(
    f"{API_BASE}/actors",
    json=new_actor,
    headers=headers
)
created_actor = response.json()
```

2. GraphQL API:
```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Setup client
transport = RequestsHTTPTransport(
    url='https://api.stasis.org/graphql',
    headers={'Authorization': f'Bearer {API_KEY}'}
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Query actor details
query = gql("""
    query GetActor($id: ID!) {
        actor(id: $id) {
            name
            aliases
            technical_profile {
                capability_level
                tools_malware {
                    name
                    type
                }
            }
            behavioral_analysis {
                target_sectors
                geographic_targeting
            }
        }
    }
""")

result = client.execute(query, variable_values={
    "id": "TA23CHN-APT001"
})

# Search actors
query = gql("""
    query SearchActors($criteria: ActorSearchInput!) {
        searchActors(criteria: $criteria) {
            actors {
                id
                name
                confidence_level
            }
            total
        }
    }
""")

result = client.execute(query, variable_values={
    "criteria": {
        "capability_level": "Advanced",
        "target_sectors": ["Technology"],
        "confidence_minimum": 3
    }
})
```

### Production Deployment Guide

1. Environment Setup:
```bash
# Create production configuration
cp config/config.example.yaml config/config.production.yaml

# Set up environment variables
export STASIS_ENV=production
export STASIS_CONFIG_PATH=/etc/stasis/config.yaml
export STASIS_DB_PASSWORD=secure-password
```

2. Docker Deployment:
```yaml
# docker-compose.production.yml
version: '3.8'

services:
  app:
    image: stasis:latest
    environment:
      - STASIS_ENV=production
      - STASIS_CONFIG_PATH=/etc/stasis/config.yaml
    volumes:
      - /etc/stasis:/etc/stasis
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      - POSTGRES_PASSWORD=${STASIS_DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:6
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

3. Monitoring Setup:
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'stasis'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

4. Logging Configuration:
```yaml
# logging.production.yaml
version: 1
disable_existing_loggers: false

formatters:
  json:
    class: pythonjsonlogger.jsonlogger.JsonFormatter
    format: '%(asctime)s %(name)s %(levelname)s %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    formatter: json
    stream: ext://sys.stdout

  file:
    class: logging.handlers.RotatingFileHandler
    formatter: json
    filename: /var/log/stasis/app.log
    maxBytes: 10485760  # 10MB
    backupCount: 10

loggers:
  '':  # Root logger
    level: INFO
    handlers: [console, file]
    propagate: true
```

5. Backup Configuration:
```yaml
# backup.production.yaml
backups:
  database:
    schedule: "0 2 * * *"  # Daily at 2 AM
    retention_days: 30
    storage:
      type: s3
      bucket: stasis-backups
      path: /database
      credentials:
        aws_access_key_id: ${AWS_ACCESS_KEY_ID}
        aws_secret_access_key: ${AWS_SECRET_ACCESS_KEY}
        region: us-east-1

  actor_data:
    schedule: "0 3 * * *"  # Daily at 3 AM
    format: json
    storage:
      type: s3
      bucket: stasis-backups
      path: /actors
```

### Security Considerations

1. API Security:
```python
# api/security.py
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not is_valid_api_key(api_key):
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

def is_valid_api_key(api_key: str) -> bool:
    # Implement API key validation logic
    pass
```

2. Data Encryption:
```python
# utils/encryption.py
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

class DataEncryption:
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt_data(self, data: dict) -> dict:
        """Encrypt sensitive fields in the data dictionary."""
        encrypted_data = data.copy()
        for field in self.SENSITIVE_FIELDS:
            if field in encrypted_data:
                encrypted_data[field] = self.encrypt_value(
                    encrypted_data[field]
                )
        return encrypted_data

    def decrypt_data(self, data: dict) -> dict:
        """Decrypt sensitive fields in the data dictionary."""
        decrypted_data = data.copy()
        for field in self.SENSITIVE_FIELDS:
            if field in decrypted_data:
                decrypted_data[field] = self.decrypt_value(
                    decrypted_data[field]
                )
        return decrypted_data

    SENSITIVE_FIELDS = [
        "infrastructure.credentials",
        "api_keys",
        "source_tokens"
    ]
```

3. Access Control:
```python
# utils/access_control.py
from enum import Enum
from typing import List

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class AccessControl:
    def __init__(self):
        self.role_permissions = {
            "analyst": [Permission.READ],
            "researcher": [Permission.READ, Permission.WRITE],
            "admin": [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN]
        }

    def check_permission(self, user_role: str, required_permission: Permission) -> bool:
        """Check if user role has required permission."""
        if user_role not in self.role_permissions:
            return False
        return required_permission in self.role_permissions[user_role]

    def get_user_permissions(self, user_role: str) -> List[Permission]:
        """Get list of permissions for user role."""
        return self.role_permissions.get(user_role, [])

    def require_permission(self, user_role: str, required_permission: Permission):
        """Decorator to require specific permission."""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                if not self.check_permission(user_role, required_permission):
                    raise PermissionError(
                        f"User role {user_role} does not have {required_permission.value} permission"
                    )
                return await func(*args, **kwargs)
            return wrapper
        return decorator
```

### Data Quality Management

1. Validation Rules:
```python
# validation/rules.py
from typing import Any, Dict, List
from datetime import datetime

class ValidationRule:
    def __init__(self, field: str, rule_type: str, parameters: Dict[str, Any] = None):
        self.field = field
        self.rule_type = rule_type
        self.parameters = parameters or {}

    def validate(self, value: Any) -> bool:
        if self.rule_type == "required":
            return value is not None and value != ""
        elif self.rule_type == "enum":
            return value in self.parameters.get("values", [])
        elif self.rule_type == "date":
            try:
                datetime.fromisoformat(value)
                return True
            except (ValueError, TypeError):
                return False
        elif self.rule_type == "regex":
            import re
            pattern = self.parameters.get("pattern")
            return bool(re.match(pattern, str(value)))
        return True

class ValidationRuleSet:
    def __init__(self):
        self.rules: Dict[str, List[ValidationRule]] = {
            "actor_id": [
                ValidationRule("actor_id", "required"),
                ValidationRule("actor_id", "regex", {"pattern": r"^TA\d{2}[A-Z]{3}-[A-Z]{3}\d{3}$"})
            ],
            "name": [
                ValidationRule("name", "required")
            ],
            "confidence_level": [
                ValidationRule("confidence_level", "required"),
                ValidationRule("confidence_level", "enum", {"values": [1, 2, 3, 4, 5]})
            ],
            "capability_level": [
                ValidationRule("capability_level", "enum", {"values": ["Basic", "Intermediate", "Advanced"]})
            ]
        }

    def validate_field(self, field: str, value: Any) -> bool:
        """Validate a single field against its rules."""
        if field not in self.rules:
            return True
        
        return all(rule.validate(value) for rule in self.rules[field])

    def validate_actor(self, actor_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate entire actor data, return dictionary of validation errors."""
        errors = {}
        
        for field, rules in self.rules.items():
            field_value = actor_data.get(field)
            failed_rules = [
                rule.rule_type for rule in rules 
                if not rule.validate(field_value)
            ]
            
            if failed_rules:
                errors[field] = failed_rules
                
        return errors
```

2. Data Quality Metrics:
```python
# quality/metrics.py
from typing import Dict, List
from datetime import datetime, timedelta

class DataQualityMetrics:
    """Calculate and track data quality metrics."""
    
    def __init__(self, actor_data: Dict[str, Any]):
        self.actor_data = actor_data
        self.metrics = {}

    def calculate_completeness(self) -> float:
        """Calculate the completeness score of the actor data."""
        required_fields = [
            "actor_id", "name", "first_observed", "confidence_level",
            "capability_level", "motivation"
        ]
        
        optional_fields = [
            "last_observed", "aliases", "tools_malware", "infrastructure",
            "target_sectors", "geographic_targeting", "attack_patterns",
            "goals", "relationships"
        ]

        required_count = sum(1 for field in required_fields if self.actor_data.get(field))
        optional_count = sum(1 for field in optional_fields if self.actor_data.get(field))
        
        required_score = required_count / len(required_fields)
        optional_score = optional_count / len(optional_fields)
        
        return (required_score * 0.7) + (optional_score * 0.3)

    def calculate_timeliness(self) -> float:
        """Calculate the timeliness score of the actor data."""
        current_time = datetime.now()
        last_updated = datetime.fromisoformat(self.actor_data.get('metadata', {}).get('modified', current_time.isoformat()))
        
        # Score decreases over time since last update
        days_since_update = (current_time - last_updated).days
        if days_since_update <= 30:
            return 1.0
        elif days_since_update <= 90:
            return 0.75
        elif days_since_update <= 180:
            return 0.5
        else:
            return 0.25

    def calculate_accuracy(self) -> float:
        """Calculate the accuracy score based on confidence levels and references."""
        confidence_score = self.actor_data.get('confidence_level', 0) / 5.0
        
        # Check reference quality
        references = self.actor_data.get('references', [])
        if not references:
            reference_score = 0.0
        else:
            reference_scores = []
            for ref in references:
                score = 0.0
                if ref.get('url'):
                    score += 0.3
                if ref.get('title'):
                    score += 0.2
                if ref.get('source'):
                    score += 0.3
                if ref.get('date'):
                    score += 0.2
                reference_scores.append(score)
            reference_score = sum(reference_scores) / len(reference_scores)
        
        return (confidence_score * 0.6) + (reference_score * 0.4)

    def calculate_consistency(self) -> float:
        """Calculate the consistency score of the actor data."""
        consistency_checks = [
            self._check_date_consistency(),
            self._check_relationship_consistency(),
            self._check_technical_consistency()
        ]
        
        return sum(consistency_checks) / len(consistency_checks)

    def _check_date_consistency(self) -> float:
        """Check consistency of dates in the actor data."""
        try:
            first_observed = datetime.fromisoformat(self.actor_data.get('first_observed', ''))
            last_observed = datetime.fromisoformat(self.actor_data.get('last_observed', '')) if self.actor_data.get('last_observed') else None
            
            if last_observed and last_observed < first_observed:
                return 0.0
            
            return 1.0
        except ValueError:
            return 0.0

    def _check_relationship_consistency(self) -> float:
        """Check consistency of relationship data."""
        relationships = self.actor_data.get('relationships', [])
        if not relationships:
            return 1.0

        valid_relationships = 0
        for relationship in relationships:
            if all(k in relationship for k in ['related_actor', 'relationship_type', 'confidence']):
                if relationship['confidence'] >= 1 and relationship['confidence'] <= 5:
                    valid_relationships += 1

        return valid_relationships / len(relationships)

    def _check_technical_consistency(self) -> float:
        """Check consistency of technical data."""
        technical_profile = self.actor_data.get('technical_profile', {})
        
        checks = []
        
        # Check capability level matches tools sophistication
        if technical_profile.get('capability_level') == 'Advanced':
            tools = technical_profile.get('tools_malware', [])
            custom_tools = sum(1 for tool in tools if tool.get('type') == 'Custom')
            checks.append(custom_tools > 0)

        # Check infrastructure matches capability
        if technical_profile.get('infrastructure'):
            infra_sophistication = technical_profile['infrastructure'].get('sophistication', 'Basic')
            capability_level = technical_profile.get('capability_level', 'Basic')
            checks.append(
                (infra_sophistication == 'Advanced' and capability_level == 'Advanced') or
                (infra_sophistication != 'Advanced')
            )

        return sum(checks) / len(checks) if checks else 1.0

    def generate_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive data quality report."""
        completeness = self.calculate_completeness()
        timeliness = self.calculate_timeliness()
        accuracy = self.calculate_accuracy()
        consistency = self.calculate_consistency()

        overall_score = (
            completeness * 0.3 +
            timeliness * 0.2 +
            accuracy * 0.3 +
            consistency * 0.2
        )

        return {
            "actor_id": self.actor_data.get('actor_id'),
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "completeness": {
                    "score": completeness,
                    "details": self._get_completeness_details()
                },
                "timeliness": {
                    "score": timeliness,
                    "last_updated": self.actor_data.get('metadata', {}).get('modified')
                },
                "accuracy": {
                    "score": accuracy,
                    "confidence_level": self.actor_data.get('confidence_level'),
                    "reference_count": len(self.actor_data.get('references', []))
                },
                "consistency": {
                    "score": consistency,
                    "checks": {
                        "dates": self._check_date_consistency(),
                        "relationships": self._check_relationship_consistency(),
                        "technical": self._check_technical_consistency()
                    }
                }
            },
            "overall_score": overall_score,
            "recommendations": self._generate_recommendations()
        }

    def _get_completeness_details(self) -> Dict[str, Any]:
        """Get detailed completeness information."""
        missing_fields = []
        partial_fields = []
        
        for field, value in self.actor_data.items():
            if value is None or value == "" or value == [] or value == {}:
                missing_fields.append(field)
            elif isinstance(value, (list, dict)) and len(value) < 2:
                partial_fields.append(field)

        return {
            "missing_fields": missing_fields,
            "partial_fields": partial_fields,
            "completion_rate": f"{self.calculate_completeness()*100:.1f}%"
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for improving data quality."""
        recommendations = []
        
        # Completeness recommendations
        completeness = self.calculate_completeness()
        if completeness < 0.8:
            missing_details = self._get_completeness_details()
            if missing_details['missing_fields']:
                recommendations.append(
                    f"Add missing information for fields: {', '.join(missing_details['missing_fields'])}"
                )
            if missing_details['partial_fields']:
                recommendations.append(
                    f"Enhance information for fields with minimal data: {', '.join(missing_details['partial_fields'])}"
                )

        # Timeliness recommendations
        timeliness = self.calculate_timeliness()
        if timeliness < 0.7:
            last_updated = datetime.fromisoformat(
                self.actor_data.get('metadata', {}).get('modified', datetime.now().isoformat())
            )
            days_since_update = (datetime.now() - last_updated).days
            recommendations.append(
                f"Update actor information (last updated {days_since_update} days ago)"
            )

        # Accuracy recommendations
        accuracy = self.calculate_accuracy()
        if accuracy < 0.7:
            if self.actor_data.get('confidence_level', 0) < 3:
                recommendations.append(
                    "Improve confidence level by adding more supporting evidence"
                )
            if len(self.actor_data.get('references', [])) < 2:
                recommendations.append(
                    "Add more references to support actor information"
                )

        # Consistency recommendations
        consistency = self.calculate_consistency()
        if consistency < 0.7:
            if not self._check_date_consistency():
                recommendations.append(
                    "Review and correct date inconsistencies"
                )
            if not self._check_relationship_consistency():
                recommendations.append(
                    "Review and validate relationship information"
                )
            if not self._check_technical_consistency():
                recommendations.append(
                    "Review technical profile for consistency with stated capabilities"
                )

        return recommendations

    def export_metrics(self, format: str = 'json') -> str:
        """Export quality metrics in specified format."""
        report = self.generate_quality_report()
        
        if format.lower() == 'json':
            return json.dumps(report, indent=2)
            
        elif format.lower() == 'markdown':
            md_lines = [
                f"# Data Quality Report - {report['actor_id']}",
                f"\nGenerated: {report['timestamp']}",
                f"\n## Overall Score: {report['overall_score']:.2f}",
                "\n## Metrics",
                "\n### Completeness",
                f"- Score: {report['metrics']['completeness']['score']:.2f}",
                f"- Missing Fields: {', '.join(report['metrics']['completeness']['details']['missing_fields'])}",
                f"- Partial Fields: {', '.join(report['metrics']['completeness']['details']['partial_fields'])}",
                "\n### Timeliness",
                f"- Score: {report['metrics']['timeliness']['score']:.2f}",
                f"- Last Updated: {report['metrics']['timeliness']['last_updated']}",
                "\n### Accuracy",
                f"- Score: {report['metrics']['accuracy']['score']:.2f}",
                f"- Confidence Level: {report['metrics']['accuracy']['confidence_level']}",
                f"- Reference Count: {report['metrics']['accuracy']['reference_count']}",
                "\n### Consistency",
                f"- Score: {report['metrics']['consistency']['score']:.2f}",
                "\n## Recommendations",
                "\n".join(f"- {rec}" for rec in report['recommendations'])
            ]
            return "\n".join(md_lines)
            
        else:
            raise ValueError(f"Unsupported export format: {format}")

class QualityMonitor:
    """Monitor and track data quality over time."""
    
    def __init__(self, db_connection):
        """Initialize quality monitor with database connection."""
        self.db = db_connection
        self.metrics_history = {}
        self.alert_thresholds = {
            'completeness': 0.7,
            'timeliness': 0.7,
            'accuracy': 0.7,
            'consistency': 0.7,
            'overall': 0.7
        }

    async def monitor_actor_quality(self, actor_id: str) -> Dict[str, Any]:
        """Monitor quality metrics for a specific actor."""
        try:
            # Fetch actor data
            actor_data = await self.db.get_actor(actor_id)
            if not actor_data:
                raise ValueError(f"Actor not found: {actor_id}")

            # Calculate current metrics
            metrics = DataQualityMetrics(actor_data)
            current_report = metrics.generate_quality_report()

            # Store metrics history
            await self._store_metrics_history(actor_id, current_report)

            # Check for alerts
            alerts = self._check_quality_alerts(current_report)

            # Generate trend analysis
            trends = await self._analyze_trends(actor_id)

            return {
                "current_metrics": current_report,
                "alerts": alerts,
                "trends": trends
            }

        except Exception as e:
            logger.error(f"Error monitoring actor quality: {str(e)}")
            raise

    async def _store_metrics_history(self, actor_id: str, metrics: Dict[str, Any]):
        """Store metrics history in database."""
        try:
            await self.db.store_metrics(
                actor_id=actor_id,
                timestamp=datetime.now(),
                metrics=metrics
            )
        except Exception as e:
            logger.error(f"Error storing metrics history: {str(e)}")
            raise

    def _check_quality_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for quality metric alerts."""
        alerts = []

        for metric, threshold in self.alert_thresholds.items():
            if metric == 'overall':
                current_value = metrics['overall_score']
            else:
                current_value = metrics['metrics'][metric]['score']

            if current_value < threshold:
                alerts.append({
                    "type": f"low_{metric}_score",
                    "metric": metric,
                    "current_value": current_value,
                    "threshold": threshold,
                    "timestamp": datetime.now().isoformat()
                })

        return alerts

    async def _analyze_trends(self, actor_id: str) -> Dict[str, Any]:
        """Analyze quality metric trends over time."""
        try:
            # Fetch historical metrics
            history = await self.db.get_metrics_history(
                actor_id=actor_id,
                start_date=datetime.now() - timedelta(days=90)
            )

            trends = {
                "completeness": self._calculate_trend([h['metrics']['completeness']['score'] for h in history]),
                "timeliness": self._calculate_trend([h['metrics']['timeliness']['score'] for h in history]),
                "accuracy": self._calculate_trend([h['metrics']['accuracy']['score'] for h in history]),
                "consistency": self._calculate_trend([h['metrics']['consistency']['score'] for h in history]),
                "overall": self._calculate_trend([h['overall_score'] for h in history])
            }

            return trends

        except Exception as e:
            logger.error(f"Error analyzing trends: {str(e)}")
            raise

    def _calculate_trend(self, values: List[float]) -> Dict[str, Any]:
        """Calculate trend statistics for a metric."""
        if not values:
            return {
                "direction": "stable",
                "change_rate": 0.0,
                "volatility": 0.0
            }

        # Calculate direction and change rate
        change_rate = (values[-1] - values[0]) / len(values)
        
        # Determine trend direction
        if change_rate > 0.01:
            direction = "improving"
        elif change_rate < -0.01:
            direction = "declining"
        else:
            direction = "stable"

        # Calculate volatility (standard deviation)
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        volatility = variance ** 0.5

        return {
            "direction": direction,
            "change_rate": change_rate,
            "volatility": volatility,
            "current": values[-1],
            "previous": values[0],
            "min": min(values),
            "max": max(values)
        }

    async def generate_quality_report(self, actor_id: str, format: str = 'json') -> str:
        """Generate comprehensive quality report."""
        monitoring_data = await self.monitor_actor_quality(actor_id)
        
        if format.lower() == 'json':
            return json.dumps(monitoring_data, indent=2)
            
        elif format.lower() == 'markdown':
            md_lines = [
                f"# Quality Monitoring Report - {actor_id}",
                f"\nGenerated: {datetime.now().isoformat()}",
                
                "\n## Current Metrics",
                f"Overall Score: {monitoring_data['current_metrics']['overall_score']:.2f}",
                
                "\n### Individual Metrics",
                f"- Completeness: {monitoring_data['current_metrics']['metrics']['completeness']['score']:.2f}",
                f"- Timeliness: {monitoring_data['current_metrics']['metrics']['timeliness']['score']:.2f}",
                f"- Accuracy: {monitoring_data['current_metrics']['metrics']['accuracy']['score']:.2f}",
                f"- Consistency: {monitoring_data['current_metrics']['metrics']['consistency']['score']:.2f}",
                
                "\n## Alerts",
                *(f"- {alert['type']}: {alert['current_value']:.2f} (threshold: {alert['threshold']:.2f})" 
                  for alert in monitoring_data['alerts']),
                
                "\n## Trends",
                "\n### Completeness",
                f"- Direction: {monitoring_data['trends']['completeness']['direction']}",
                f"- Change Rate: {monitoring_data['trends']['completeness']['change_rate']:.3f}",
                f"- Volatility: {monitoring_data['trends']['completeness']['volatility']:.3f}",
                
                "\n### Timeliness",
                f"- Direction: {monitoring_data['trends']['timeliness']['direction']}",
                f"- Change Rate: {monitoring_data['trends']['timeliness']['change_rate']:.3f}",
                f"- Volatility: {monitoring_data['trends']['timeliness']['volatility']:.3f}",
                
                "\n### Accuracy",
                f"- Direction: {monitoring_data['trends']['accuracy']['direction']}",
                f"- Change Rate: {monitoring_data['trends']['accuracy']['change_rate']:.3f}",
                f"- Volatility: {monitoring_data['trends']['accuracy']['volatility']:.3f}",
                
                "\n### Consistency",
                f"- Direction: {monitoring_data['trends']['consistency']['direction']}",
                f"- Change Rate: {monitoring_data['trends']['consistency']['change_rate']:.3f}",
                f"- Volatility: {monitoring_data['trends']['consistency']['volatility']:.3f}",
                
                "\n## Recommendations",
                *(f"- {rec}" for rec in monitoring_data['current_metrics']['recommendations'])
            ]
            
            return "\n".join(md_lines)
        
        else:
            raise ValueError(f"Unsupported report format: {format}")

    async def set_alert_threshold(self, metric: str, threshold: float):
        """Set alert threshold for a specific metric."""
        if metric not in self.alert_thresholds:
            raise ValueError(f"Invalid metric: {metric}")
        
        if not 0 <= threshold <= 1:
            raise ValueError("Threshold must be between 0 and 1")
            
        self.alert_thresholds[metric] = threshold
        
        # Store updated thresholds in database
        await self.db.store_thresholds(self.alert_thresholds)

    async def get_quality_statistics(self, timeframe: str = '30d') -> Dict[str, Any]:
        """Get quality statistics across all actors."""
        try:
            # Calculate timeframe
            end_date = datetime.now()
            if timeframe.endswith('d'):
                days = int(timeframe[:-1])
                start_date = end_date - timedelta(days=days)
            elif timeframe.endswith('m'):
                months = int(timeframe[:-1])
                start_date = end_date - timedelta(days=months*30)
            else:
                raise ValueError(f"Invalid timeframe format: {timeframe}")

            # Fetch metrics for all actors
            all_metrics = await self.db.get_all_metrics(
                start_date=start_date,
                end_date=end_date
            )

            # Calculate statistics
            stats = {
                "overall": {
                    "average": self._calculate_average([m['overall_score'] for m in all_metrics]),
                    "median": self._calculate_median([m['overall_score'] for m in all_metrics]),
                    "std_dev": self._calculate_std_dev([m['overall_score'] for m in all_metrics])
                }
            }

            # Calculate for each metric
            for metric in ['completeness', 'timeliness', 'accuracy', 'consistency']:
                values = [m['metrics'][metric]['score'] for m in all_metrics]
                stats[metric] = {
                    "average": self._calculate_average(values),
                    "median": self._calculate_median(values),
                    "std_dev": self._calculate_std_dev(values)
                }

            return stats

        except Exception as e:
            logger.error(f"Error calculating quality statistics: {str(e)}")
            raise

    def _calculate_average(self, values: List[float]) -> float:
        """Calculate average of values."""
        return sum(values) / len(values) if values else 0.0

    def _calculate_median(self, values: List[float]) -> float:
        """Calculate median of values."""
        sorted_values = sorted(values)
        n = len(sorted_values)
        mid = n // 2
        
        if n % 2 == 0:
            return (sorted_values[mid-1] + sorted_values[mid]) / 2
        return sorted_values[mid]

    def _calculate_std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation of values."""
        if not values:
            return 0.0
            
        avg = self._calculate_average(values)
        variance = sum((x - avg) ** 2 for x in values) / len(values)
        return variance ** 0.5

    async def export_quality_dashboard(self) -> Dict[str, Any]:
        """Generate quality dashboard data."""
        try:
            # Get current statistics
            current_stats = await self.get_quality_statistics('30d')
            
            # Get historical trends
            historical_trends = await self.get_quality_statistics('90d')
            
            # Get actors needing attention
            attention_needed = await self._get_actors_needing_attention()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "current_statistics": current_stats,
                "historical_trends": historical_trends,
                "attention_needed": attention_needed,
                "metrics_summary": {
                    "total_actors": await self.db.count_actors(),
                    "actors_updated_30d": await self.db.count_actors_updated_since(
                        datetime.now() - timedelta(days=30)
                    ),
                    "average_quality_score": current_stats['overall']['average'],
                    "quality_trend": self._compare_trends(
                        current_stats['overall']['average'],
                        historical_trends['overall']['average']
                    )
                },
                "recommendations": await self._generate_dashboard_recommendations()
            }

        except Exception as e:
            logger.error(f"Error generating quality dashboard: {str(e)}")
            raise

    async def _get_actors_needing_attention(self) -> List[Dict[str, Any]]:
        """Identify actors needing quality improvements."""
        try:
            all_actors = await self.db.get_all_actors()
            attention_needed = []

            for actor in all_actors:
                metrics = DataQualityMetrics(actor)
                report = metrics.generate_quality_report()

                if report['overall_score'] < self.alert_thresholds['overall']:
                    attention_needed.append({
                        "actor_id": actor['actor_id'],
                        "name": actor['name'],
                        "overall_score": report['overall_score'],
                        "last_updated": actor.get('metadata', {}).get('modified'),
                        "critical_issues": [
                            metric for metric, threshold in self.alert_thresholds.items()
                            if report['metrics'].get(metric, {}).get('score', 0) < threshold
                        ],
                        "recommendations": report['recommendations'][:3]  # Top 3 recommendations
                    })

            # Sort by overall score ascending (worst first)
            return sorted(attention_needed, key=lambda x: x['overall_score'])

        except Exception as e:
            logger.error(f"Error identifying actors needing attention: {str(e)}")
            raise

    def _compare_trends(self, current: float, historical: float) -> str:
        """Compare current vs historical values to determine trend."""
        diff = current - historical
        if abs(diff) < 0.01:
            return "stable"
        return "improving" if diff > 0 else "declining"

    async def _generate_dashboard_recommendations(self) -> List[str]:
        """Generate overall recommendations for quality improvement."""
        try:
            stats = await self.get_quality_statistics('30d')
            recommendations = []

            # Check overall quality
            if stats['overall']['average'] < 0.8:
                recommendations.append(
                    "Overall quality score is below target. Consider implementing systematic quality improvement program."
                )

            # Check individual metrics
            for metric in ['completeness', 'timeliness', 'accuracy', 'consistency']:
                if stats[metric]['average'] < self.alert_thresholds[metric]:
                    recommendations.append(
                        f"Average {metric} score is below threshold. Focus on improving {metric} across all actors."
                    )

            # Check variability
            high_variability_metrics = [
                metric for metric in ['completeness', 'timeliness', 'accuracy', 'consistency']
                if stats[metric]['std_dev'] > 0.2
            ]
            if high_variability_metrics:
                recommendations.append(
                    f"High variability detected in {', '.join(high_variability_metrics)}. "
                    "Consider standardizing data collection processes."
                )

            # Add general recommendations
            recommendations.extend([
                "Regularly review and update actor profiles",
                "Validate all new information against multiple sources",
                "Document changes and updates comprehensively"
            ])

            return recommendations

        except Exception as e:
            logger.error(f"Error generating dashboard recommendations: {str(e)}")
            raise

    async def schedule_quality_checks(self, interval: int = 24):
        """Schedule regular quality checks (interval in hours)."""
        while True:
            try:
                # Generate quality reports for all actors
                all_actors = await self.db.get_all_actors()
                for actor in all_actors:
                    report = await self.monitor_actor_quality(actor['actor_id'])
                    
                    # Store report
                    await self.db.store_quality_report(
                        actor_id=actor['actor_id'],
                        report=report,
                        timestamp=datetime.now()
                    )
                    
                    # Check for alerts
                    if report['alerts']:
                        await self._send_quality_alerts(actor['actor_id'], report['alerts'])

                # Generate and store dashboard
                dashboard = await self.export_quality_dashboard()
                await self.db.store_dashboard(dashboard)

                # Wait for next check
                await asyncio.sleep(interval * 3600)

            except Exception as e:
                logger.error(f"Error in scheduled quality check: {str(e)}")
                await asyncio.sleep(300)  # Wait 5 minutes before retry

    async def _send_quality_alerts(self, actor_id: str, alerts: List[Dict[str, Any]]):
        """Send alerts for quality issues."""
        try:
            for alert in alerts:
                await self.db.store_alert(
                    actor_id=actor_id,
                    alert_type=alert['type'],
                    alert_data=alert,
                    timestamp=datetime.now()
                )
                
                # Send notification (implement according to your notification system)
                await self._send_notification(
                    title=f"Quality Alert - {actor_id}",
                    message=f"Quality issue detected: {alert['type']} - Current value: {alert['current_value']:.2f}"
                )

        except Exception as e:
            logger.error(f"Error sending quality alerts: {str(e)}")
            raise
```

Now, let's complete the README.md with the final sections:

```markdown
## Advanced Usage

### Quality Monitoring

The system includes comprehensive quality monitoring capabilities:

```python
from stasis.quality import QualityMonitor

# Initialize monitor
monitor = QualityMonitor(db_connection)

# Monitor specific actor
report = await monitor.monitor_actor_quality("TA23CHN-APT001")

# Generate quality dashboard
dashboard = await monitor.export_quality_dashboard()

# Set custom alert thresholds
await monitor.set_alert_threshold("completeness", 0.8)
```

### Automated Updates

Schedule regular updates and quality checks:

```python
from stasis import AutomationManager

manager = AutomationManager()

# Schedule source updates
await manager.schedule_source_updates()

# Schedule quality checks
await manager.schedule_quality_checks()
```

## Production Considerations

### Scaling
- Use connection pooling for database connections
- Implement caching for frequently accessed data
- Consider sharding for large datasets
- Use load balancing for API endpoints

### Security
- Implement API key rotation
- Regular security audits
- Data encryption at rest
- Secure communication channels

### Monitoring
- Set up logging aggregation
- Monitor system metrics
- Configure alerts
- Regular backup verification

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Make your changes
5. Run tests:
   ```bash
   pytest
   ```
6. Submit a pull request

### Code Style
- Follow PEP 8
- Use type hints
- Write comprehensive docstrings
- Include tests for new features

## Support

- Documentation: [https://docs.stasis-project.org](https://docs.stasis-project.org)
- Issues: [GitHub Issues](https://github.com/your-org/stasis/issues)
- Discussions: [GitHub Discussions](https://github.com/your-org/stasis/discussions)
- Email: support@stasis-project.org
- Community Chat: [Discord](https://discord.gg/stasis)

## FAQ

### General Questions

**Q: How does STASIS differ from other threat intelligence platforms?**
A: STASIS focuses specifically on threat actor profiling with a standardized, extensible schema. It emphasizes data quality, relationship mapping, and comprehensive actor profiles while maintaining strict validation and reference requirements.

**Q: Can I integrate STASIS with existing tools?**
A: Yes, STASIS provides multiple integration options:
- REST and GraphQL APIs
- STIX 2.1 export
- Custom source integration
- Webhook support

**Q: How can I contribute to the project?**
A: We welcome contributions in various forms:
- Code contributions
- Documentation improvements
- Bug reports
- Feature requests
- Custom source implementations

### Technical Questions

**Q: What databases are supported?**
A: STASIS supports:
- MongoDB
- PostgreSQL
- File-based storage
- Custom storage backends (via plugin system)

**Q: How is data quality maintained?**
A: Through multiple mechanisms:
- Strict schema validation
- Required source references
- Confidence scoring
- Regular quality checks
- Automated monitoring

**Q: Can I add custom data fields?**
A: Yes, through:
- Custom extensions
- Flexible metadata
- Plugin system
- Custom source implementations

## License

Copyright (c) 2023 STASIS Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this software except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Acknowledgments

### Projects
- MITRE ATT&CK®
- STIX™
- TAXII™
- CybOX™

### Contributors
- Core Development Team
- Community Contributors
- Security Researchers

### Organizations
- Partner Organizations
- Research Institutions
- Security Vendors

## Changelog

### 1.0.0 (2023-12-01)
- Initial release
- Core functionality
- Basic integrations
- Documentation

### 1.0.1 (2023-12-15)
- Bug fixes
- Documentation updates
- Performance improvements
- Additional data sources

### 1.1.0 (Planned - 2024-Q1)
- Enhanced ML capabilities
- Advanced visualization
- Additional integrations
- Improved automation

## Roadmap

### Short Term (Q1 2024)
- Enhanced machine learning integration
- Advanced relationship mapping
- Improved visualization tools
- Additional data source integrations

### Medium Term (Q2-Q3 2024)
- Real-time collaboration features
- Advanced analytics dashboard
- Automated report generation
- Enhanced API capabilities

### Long Term (Q4 2024+)
- AI-powered analysis
- Predictive capabilities
- Advanced automation
- Extended integration options

## Contact

### General Inquiries
- Email: info@stasis-project.org
- Website: https://stasis-project.org

### Technical Support
- Email: support@stasis-project.org
- Documentation: https://docs.stasis-project.org
- GitHub Issues: https://github.com/your-org/stasis/issues

### Security Issues
- Email: security@stasis-project.org
- PGP Key: [Download](https://stasis-project.org/security/pgp-key.asc)

---

STASIS - Structured Threat Actor Schema & Intelligence System