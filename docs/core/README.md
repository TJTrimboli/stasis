# STASIS Core Components

## Overview
The core components of the Structured Threat Actor Schema & Intelligence System (STASIS) provide the fundamental building blocks for threat actor profiling and intelligence management. These components establish the base structure for identification, classification, and relationship mapping of threat actors.

## Components

### Identification
- [Detailed Documentation](./identification.md)
- Provides unique identification and naming conventions
- Manages threat actor aliases and alternative names
- Tracks first and last observed dates
- Includes confidence scoring for attribution

### Technical Profile
- [Detailed Documentation](./technical-profile.md)
- Defines capability assessment framework
- Documents tools and malware usage
- Maps infrastructure patterns
- Records exploitation methods

### Behavioral Analysis
- [Detailed Documentation](./behavioral-analysis.md)
- Captures targeting patterns
- Documents geographic focus
- Records attack patterns
- Analyzes temporal behaviors

### Strategic Context
- [Detailed Documentation](./strategic-context.md)
- Defines motivations and goals
- Maps relationships with other actors
- Assesses resource capabilities
- Tracks strategic evolution

## Implementation
### Core Identifier Format
```
TA{YY}{XXX}-{CAT}{NUM}
```
- `TA`: Fixed prefix indicating "Threat Actor"
- `YY`: Two-digit year of first observation
- `XXX`: Three-letter geographic origin code (ISO 3166-1)
- `CAT`: Category code (APT/CRM/HAC)
- `NUM`: Sequential three-digit number

### Required Fields
All core components must include:
- Unique identifier (unique_id)
- First observed date (first_observed)
- Confidence level (confidence_level)
- Last modified timestamp (last_active)
- Status of operation (status)

### Confidence Scoring
STASIS implements a standardized 1-5 confidence scale:
1. Low: Limited evidence, high uncertainty
2. Low-Medium: Some evidence, significant uncertainty
3. Medium: Moderate evidence, reasonable confidence
4. Medium-High: Strong evidence, high confidence
5. High: Extensive evidence, very high confidence

### Versioning
Version numbers follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

## Usage Guidelines

### Creating New Profiles
1. Generate unique identifier following STASIS format
2. Complete all required fields
3. Document confidence levels
4. Include supporting evidence
5. Set appropriate TLP level

### Updating Existing Profiles
1. Increment version number
2. Update modified timestamp
3. Document changes
4. Maintain change history
5. Review confidence levels

### Quality Control
- Regular review of profiles
- Validation against schema
- Cross-reference checking
- Confidence assessment review
- Evidence validation

## Implementation Guidelines

### Basic Usage
```json
{
    "core_identification": {
        "unique_id": "TA23CHN-APT001",
        "first_observed": "2023-01-15",
        "confidence_level": 4
    }
}
```

### Advanced Implementation
```json
{
    "core_identification": {
        "unique_id": "TA23CHN-APT001",
        "aliases": ["DragonForce", "Red Dragon"],
        "first_observed": "2023-01-15",
        "last_active": "2023-12-01",
        "confidence_level": 4,
        "status": "active"
    }
}
```

### Complete Profile
[Link to full example](./examples/complete-profile.md)

## Schema Reference
- [Core Schema Documentation](../../schemas/core/)
- [JSON Schema Definitions](../../schemas/core/threat-actor.json)

## Best Practices
1. Maintain consistent documentation
2. Regular profile updates
3. Evidence-based confidence scoring
4. Clear relationship mapping
5. Proper version control

## Related Components
- [Technical Components](../technical/)
- [Behavioral Components](../behavioral/)
- [Strategic Components](../strategic/)
- [Metadata Components](../metadata/)