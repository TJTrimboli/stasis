# STASIS Identification Component

## Overview
The identification component provides the foundational structure for uniquely identifying and tracking threat actors within the STASIS framework. This component ensures consistent and standardized identification across different organizations and platforms.

## Schema Details

### Core Properties

#### unique_id
- **Type**: string
- **Pattern**: `^TA[0-9]{2}[A-Z]{3}-[A-Z]{3}[0-9]{3}$`
- **Required**: Yes
- **Description**: Unique identifier following the STASIS naming convention
- **Example**: `TA23CHN-APT001`

#### aliases
- **Type**: array of objects
- **Required**: No
- **Description**: Collection of alternative names and identifiers
- **Properties**:
  ```json
  {
    "name": "string",
    "source": "string",
    "first_seen": "date",
    "confidence": {
      "score": 1-5,
      "justification": "string"
    }
  }
  ```

#### first_observed
- **Type**: timestamp
- **Required**: Yes
- **Description**: Date when the threat actor was first identified
- **Format**: ISO 8601 (YYYY-MM-DD)

#### last_active
- **Type**: timestamp
- **Required**: No
- **Description**: Most recent confirmed activity date
- **Format**: ISO 8601 (YYYY-MM-DD)

#### confidence_level
- **Type**: integer (1-5)
- **Required**: Yes
- **Description**: Overall confidence in the identification
- **Scale**:
  - 1: Low confidence
  - 2: Low-Medium confidence
  - 3: Medium confidence
  - 4: Medium-High confidence
  - 5: High confidence

### Status Properties

#### status
- **Type**: string
- **Required**: No
- **Allowed Values**:
  - `active`: Currently operational
  - `inactive`: No recent activity
  - `unknown`: Status cannot be determined
- **Description**: Current operational status of the threat actor

## Implementation Guide

### Creating a New Identifier

1. **Determine Components**
   ```
   TA{YY}{XXX}-{CAT}{NUM}
   ```
   - YY: Current year
   - XXX: ISO 3166-1 alpha-3 country code
   - CAT: Activity category (APT/CRM/HAC)
   - NUM: Sequential number

2. **Verify Uniqueness**
   - Check existing identifiers
   - Verify no conflicts with known aliases
   - Document decision process

3. **Set Required Fields**
   ```json
   {
     "unique_id": "TA23CHN-APT001",
     "first_observed": "2023-01-15",
     "confidence_level": 4
   }
   ```

### Managing Aliases

1. **Adding New Aliases**
   ```json
   {
     "aliases": [
       {
         "name": "DragonForce",
         "source": "Industry Report",
         "first_seen": "2023-02-01",
         "confidence": {
           "score": 4,
           "justification": "Multiple independent sources"
         }
       }
     ]
   }
   ```

2. **Alias Best Practices**
   - Document all known names
   - Include source attribution
   - Track first observation
   - Assess confidence separately
   - Regular review and updates

## Validation Rules

### Required Validations
1. Identifier format must match pattern
2. First observed date must be valid
3. Confidence level must be 1-5
4. Status must be valid enum value

### Optional Validations
1. Last active date must be after first observed
2. Aliases must have required fields
3. Sources should be documented
4. Confidence justification recommended

## Integration Guidelines

### API Endpoints

#### GET /identifiers
```http
GET /api/v1/identifiers
Accept: application/json
Authorization: Bearer {token}
```

#### POST /identifiers
```http
POST /api/v1/identifiers
Content-Type: application/json
Authorization: Bearer {token}

Request Body:
```json
{
  "unique_id": "TA23CHN-APT001",
  "first_observed": "2023-01-15",
  "confidence_level": 4,
  "aliases": [
    {
      "name": "DragonForce",
      "source": "Industry Report",
      "first_seen": "2023-02-01"
    }
  ]
}
```

### Data Exchange Format

#### STIX Mapping
```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--TA23CHN-APT001",
  "created": "2023-01-15T00:00:00.000Z",
  "modified": "2023-12-01T00:00:00.000Z",
  "name": "DragonForce",
  "aliases": ["TA23CHN-APT001"],
  "confidence": 80
}
```

#### MITRE ATT&CK Integration
```json
{
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "G0123",
      "url": "https://attack.mitre.org/groups/G0123"
    }
  ]
}
```

## Common Use Cases

### New Threat Actor Identification
1. Initial Discovery
   - Document first observation
   - Assign preliminary identifier
   - Record initial indicators
   - Set confidence level

2. Validation Process
   - Cross-reference existing actors
   - Verify unique characteristics
   - Document decision criteria
   - Update confidence assessment

### Alias Management
1. New Alias Discovery
   - Verify relationship to actor
   - Document evidence
   - Add to alias list
   - Update confidence

2. Alias Consolidation
   - Review existing aliases
   - Merge duplicates
   - Update references
   - Document changes

## Best Practices

### Identifier Assignment
1. Consistent Formatting
   - Follow pattern strictly
   - Use correct country codes
   - Maintain sequential numbering
   - Document exceptions

2. Quality Control
   - Regular validation
   - Periodic review
   - Update documentation
   - Maintain audit trail

### Confidence Assessment
1. Evidence Review
   - Technical indicators
   - Behavioral patterns
   - Historical activity
   - Source reliability

2. Regular Updates
   - New evidence review
   - Confidence reassessment
   - Documentation updates
   - Stakeholder notification

## Error Handling

### Common Issues
1. Duplicate Identifiers
   ```json
   {
     "error": "duplicate_identifier",
     "message": "Identifier TA23CHN-APT001 already exists",
     "resolution": "Verify existing entry or generate new identifier"
   }
   ```

2. Invalid Format
   ```json
   {
     "error": "invalid_format",
     "message": "Identifier does not match required pattern",
     "expected": "TA{YY}{XXX}-{CAT}{NUM}",
     "received": "TA23CH-APT001"
   }
   ```

### Resolution Procedures
1. Identifier Conflicts
   - Check existing database
   - Verify all aliases
   - Document resolution
   - Update references

2. Format Corrections
   - Validate components
   - Apply correct format
   - Update references
   - Document changes

## Maintenance Guidelines

### Regular Reviews
1. Quarterly Assessment
   - Verify active status
   - Update confidence levels
   - Review aliases
   - Document changes

2. Annual Audit
   - Comprehensive review
   - Update documentation
   - Archive inactive entries
   - Clean up references

### Version Control
1. Change Tracking
   - Document modifications
   - Update timestamps
   - Maintain history
   - Notify stakeholders

2. Archive Management
   - Regular backups
   - Version retention
   - Access control
   - Recovery procedures