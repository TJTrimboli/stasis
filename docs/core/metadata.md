# STASIS Metadata Component

## Overview
The metadata component provides essential tracking, versioning, and management information for threat actor profiles within the STASIS framework. This component ensures proper documentation, change management, and information sharing controls.

## Schema Details

### Core Metadata Properties

#### timestamps
- **Type**: object
- **Required**: Yes
- **Description**: Temporal tracking information
- **Properties**:
  ```json
  {
    "created": {
      "type": "string",
      "format": "date-time",
      "description": "Initial creation timestamp"
    },
    "modified": {
      "type": "string",
      "format": "date-time",
      "description": "Last modification timestamp"
    },
    "valid_from": {
      "type": "string",
      "format": "date-time",
      "description": "Start of validity period"
    },
    "valid_until": {
      "type": "string",
      "format": "date-time",
      "description": "End of validity period"
    }
  }
  ```

#### version_control
```json
{
  "version": {
    "type": "string",
    "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
    "description": "Semantic version number"
  },
  "revision_history": [{
    "version": "string",
    "timestamp": "date-time",
    "author": "string",
    "changes": ["string"],
    "review_status": "string"
  }]
}
```

### Information Handling

#### tlp_marking
```json
{
  "tlp_level": {
    "type": "string",
    "enum": ["WHITE", "GREEN", "AMBER", "RED"],
    "description": "Traffic Light Protocol marking"
  },
  "sharing_restrictions": [{
    "restriction_type": "string",
    "description": "string",
    "affected_parties": ["string"]
  }]
}
```

#### data_marking
```json
{
  "classification": {
    "level": "string",
    "caveats": ["string"],
    "handling_instructions": "string"
  },
  "access_control": {
    "groups": ["string"],
    "roles": ["string"],
    "organizations": ["string"]
  }
}
```

## Implementation Guide

### Metadata Management

1. **Initial Creation**
   ```json
   {
     "metadata": {
       "timestamps": {
         "created": "2023-12-01T00:00:00Z",
         "modified": "2023-12-01T00:00:00Z",
         "valid_from": "2023-12-01T00:00:00Z"
       },
       "version": "1.0.0",
       "creator": {
         "id": "analyst123",
         "organization": "STASIS"
       }
     }
   }
   ```

2. **Version Updates**
   ```json
   {
     "version_update": {
       "previous_version": "1.0.0",
       "new_version": "1.0.1",
       "timestamp": "2023-12-15T00:00:00Z",
       "author": "analyst123",
       "changes": [
         "Updated technical capabilities",
         "Added new relationship",
         "Modified confidence score"
       ],
       "review_status": "approved"
     }
   }
   ```

### Information Handling

1. **TLP Marking**
   ```json
   {
     "tlp_marking": {
       "level": "AMBER",
       "rationale": "Contains sensitive relationship details",
       "sharing_restrictions": [
         {
           "restriction_type": "Organization",
           "description": "Share only with trusted partners",
           "affected_parties": ["trusted_org_1", "trusted_org_2"]
         }
       ],
       "handling_requirements": [
         "No public disclosure",
         "Need-to-know basis",
         "Secure transmission required",
         "Track all distributions"
       ]
     }
   }
   ```

2. **Access Control**
   ```json
   {
     "access_control": {
       "classification": {
         "level": "RESTRICTED",
         "caveats": [
           "SHARING RESTRICTED",
           "SOURCE SENSITIVE"
         ],
         "handling_instructions": "Handle as TLP:AMBER"
       },
       "authorized_groups": [
         {
           "group": "senior_analysts",
           "permissions": ["read", "write", "share"]
         },
         {
           "group": "analysts",
           "permissions": ["read"]
         }
       ]
     }
   }
   ```

## Validation Rules

### Required Validations

1. **Timestamp Validation**
   - Created timestamp must be present
   - Modified timestamp must be present
   - Valid chronological order
   - ISO 8601 format compliance

2. **Version Validation**
   - Valid semantic versioning
   - Version history maintained
   - Change documentation required
   - Review status tracked

### Quality Control

1. **Metadata Completeness**
   ```json
   {
     "quality_checks": {
       "required_elements": [
         "timestamps",
         "version",
         "tlp_marking",
         "creator_info"
       ],
       "conditional_elements": [
         {
           "element": "valid_until",
           "condition": "When temporal bounds known"
         },
         {
           "element": "sharing_restrictions",
           "condition": "When TLP:AMBER or TLP:RED"
         }
       ]
     }
   }
   ```

2. **Update Requirements**
   ```json
   {
     "update_requirements": {
       "timestamp_update": "On any change",
       "version_update": "On significant change",
       "review_required": [
         "Classification change",
         "TLP level change",
         "Major version update"
       ],
       "documentation_required": [
         "Change description",
         "Update rationale",
         "Review notes"
       ]
     }
   }
   ```

## Implementation Examples

### Basic Metadata Implementation

```json
{
  "metadata": {
    "timestamps": {
      "created": "2023-12-01T00:00:00Z",
      "modified": "2023-12-15T00:00:00Z",
      "valid_from": "2023-12-01T00:00:00Z",
      "valid_until": "2024-12-01T00:00:00Z"
    },
    "version": "1.0.0",
    "creator": {
      "id": "analyst123",
      "organization": "STASIS",
      "role": "senior_analyst"
    },
    "tlp_marking": {
      "level": "AMBER",
      "sharing_restrictions": [
        {
          "type": "Organization",
          "description": "Trusted partners only"
        }
      ]
    }
  }
}
```

### Comprehensive Metadata Implementation

```json
{
  "metadata": {
    "timestamps": {
      "created": "2023-12-01T00:00:00Z",
      "modified": "2023-12-15T00:00:00Z",
      "valid_from": "2023-12-01T00:00:00Z",
      "valid_until": "2024-12-01T00:00:00Z",
      "review_date": "2024-03-01T00:00:00Z"
    },
    "version_control": {
      "current_version": "1.0.1",
      "revision_history": [
        {
          "version": "1.0.0",
          "date": "2023-12-01T00:00:00Z",
          "author": "analyst123",
          "changes": ["Initial creation"],
          "review_status": "approved",
          "reviewer": "senior_analyst456",
          "review_notes": "Complete initial profile"
        },
        {
          "version": "1.0.1",
          "date": "2023-12-15T00:00:00Z",
          "author": "analyst123",
          "changes": [
            "Updated technical capabilities",
            "Added new relationship data"
          ],
          "review_status": "approved",
          "reviewer": "senior_analyst456",
          "review_notes": "Updates validated and approved"
        }
      ]
    },
    "handling": {
      "tlp_marking": {
        "level": "AMBER",
        "rationale": "Contains sensitive relationship details",
        "sharing_restrictions": [
          {
            "type": "Organization",
            "description": "Trusted partners only",
            "authorized_organizations": [
              "trusted_org_1",
              "trusted_org_2"
            ]
          }
        ]
      },
      "access_control": {
        "classification": "RESTRICTED",
        "caveats": [
          "SHARING RESTRICTED",
          "SOURCE SENSITIVE"
        ],
        "authorized_groups": [
          "senior_analysts",
          "threat_researchers"
        ]
      }
    },
    "quality_control": {
      "last_review": {
        "date": "2023-12-15T00:00:00Z",
        "reviewer": "senior_analyst456",
        "findings": "Compliant with all requirements",
        "next_review": "2024-03-15T00:00:00Z"
      },
      "validation_status": {
        "completeness": "complete",
        "accuracy": "verified",
        "currency": "current"
      }
    }
  }
}
```

## Maintenance Guidelines

### Regular Review Cycle

1. **Monthly Reviews**
   ```markdown
   ## Monthly Metadata Review Checklist

   ### Timestamp Validation
   - [ ] All timestamps current and valid
   - [ ] Modified dates accurate
   - [ ] Review dates scheduled
   - [ ] Validity periods checked

   ### Version Control
   - [ ] Version numbers accurate
   - [ ] Change history complete
   - [ ] Review status current
   - [ ] Documentation complete

   ### Information Handling
   - [ ] TLP marking appropriate
   - [ ] Access controls current
   - [ ] Sharing restrictions valid
   - [ ] Handling instructions clear
   ```

2. **Quarterly Assessments**
   ```markdown
   ## Quarterly Metadata Assessment

   ### Comprehensive Review
   - [ ] Full version history audit
   - [ ] Access control review
   - [ ] Sharing restriction validation
   - [ ] Classification review

   ### Documentation Review
   - [ ] Change history complete
   - [ ] Review notes comprehensive
   - [ ] Handling instructions current
   - [ ] Quality control metrics
   ```

### Update Procedures

1. **Metadata Updates**
   ```json
   {
     "update_procedures": {
       "routine_updates": {
         "frequency": "As needed",
         "requirements": [
           "Update modified timestamp",
           "Document changes",
           "Validate format",
           "Check consistency"
         ]
       },
       "major_updates": {
         "frequency": "On significant changes",
         "requirements": [
           "Version number update",
           "Full review required",
           "Documentation update",
           "Approval process"
         ]
       }
     }
   }
   ```

2. **Quality Control**
   ```json
   {
     "quality_control": {
       "validation_checks": [
         {
           "type": "Format",
           "checks": [
             "Timestamp format",
             "Version format",
             "TLP marking valid"
           ]
         },
         {
           "type": "Completeness",
           "checks": [
             "Required fields present",
             "Documentation complete",
             "History maintained"
           ]
         },
         {
           "type": "Consistency",
           "checks": [
             "Version sequence valid",
             "Timestamps chronological",
             "Access controls consistent",
             "TLP marking appropriate"
           ]
         }
       ],
       "remediation_process": {
         "format_issues": {
           "priority": "High",
           "timeline": "Immediate",
           "approval": "Not required"
         },
         "completeness_issues": {
           "priority": "Medium",
           "timeline": "24 hours",
           "approval": "Team lead"
         },
         "consistency_issues": {
           "priority": "High",
           "timeline": "Immediate",
           "approval": "Senior analyst"
         }
       }
     }
   }
   ```

## Security Considerations

### Data Protection

1. **Metadata Security**
   ```json
   {
     "security_requirements": {
       "storage": {
         "encryption": "Required",
         "access_logging": "Required",
         "backup": "Daily",
         "retention": "7 years"
       },
       "transmission": {
         "encryption": "Required",
         "protocols": ["TLS 1.3"],
         "validation": "Required"
       },
       "access": {
         "authentication": "Required",
         "authorization": "Role-based",
         "audit_logging": "Required"
       }
     }
   }
   ```

2. **Handling Requirements**
   ```json
   {
     "handling_requirements": {
       "tlp_white": {
         "storage": "Standard",
         "transmission": "Any",
         "sharing": "Unrestricted"
       },
       "tlp_green": {
         "storage": "Protected",
         "transmission": "Encrypted",
         "sharing": "Community"
       },
       "tlp_amber": {
         "storage": "Secure",
         "transmission": "Encrypted",
         "sharing": "Limited"
       },
       "tlp_red": {
         "storage": "Highly Secure",
         "transmission": "Secure Channels",
         "sharing": "Named Recipients"
       }
     }
   }
   ```

## Integration Guidelines

### API Integration

1. **Metadata Endpoints**
   ```http
   GET /api/v1/metadata/{id}
   Authorization: Bearer {token}
   Accept: application/json

   Response:
   {
     "metadata": {
       "timestamps": {},
       "version_control": {},
       "handling": {},
       "quality_control": {}
     }
   }
   ```

2. **Update Endpoints**
   ```http
   PUT /api/v1/metadata/{id}
   Authorization: Bearer {token}
   Content-Type: application/json

   Request Body:
   {
     "metadata_update": {
       "modified": "2023-12-15T00:00:00Z",
       "version": "1.0.1",
       "changes": ["string"]
     }
   }
   ```

### System Integration

1. **Event Publishing**
   ```json
   {
     "metadata_events": {
       "creation": {
         "topic": "stasis.metadata.created",
         "required_fields": ["id", "timestamps", "creator"]
       },
       "update": {
         "topic": "stasis.metadata.updated",
         "required_fields": ["id", "changes", "modifier"]
       },
       "review": {
         "topic": "stasis.metadata.reviewed",
         "required_fields": ["id", "reviewer", "status"]
       }
     }
   }
   ```

2. **Synchronization**
   ```json
   {
     "sync_requirements": {
       "frequency": "Real-time",
       "validation": "Required",
       "conflict_resolution": {
         "strategy": "Latest wins",
         "exception_handling": "Manual review"
       }
     }
   }
   ```

## Appendices

### A. Metadata Field Definitions

```markdown
## Core Metadata Fields

### Timestamps
- **created**: Initial creation time (ISO 8601)
- **modified**: Last modification time (ISO 8601)
- **valid_from**: Start of validity period (ISO 8601)
- **valid_until**: End of validity period (ISO 8601)
- **review_date**: Next scheduled review (ISO 8601)

### Version Control
- **version**: Semantic version number (MAJOR.MINOR.PATCH)
- **revision_history**: List of changes and reviews
- **previous_versions**: References to earlier versions
- **deprecation_info**: Deprecation status and details

### Information Handling
- **tlp_level**: Traffic Light Protocol marking
- **classification**: Security classification
- **handling_instructions**: Special handling requirements
- **access_control**: Access restrictions and permissions

### Quality Control
- **review_status**: Current review state
- **validation_status**: Data validation state
- **completeness**: Documentation completeness
- **accuracy**: Information accuracy level

### B. Common Metadata Patterns

1. **Creation Pattern**
```json
{
  "metadata": {
    "timestamps": {
      "created": "<ISO8601>",
      "modified": "<ISO8601>",
      "valid_from": "<ISO8601>"
    },
    "version": "1.0.0",
    "creator": {
      "id": "string",
      "organization": "string"
    },
    "tlp_marking": "GREEN"
  }
}
```

2. **Update Pattern**
```json
{
  "metadata": {
    "timestamps": {
      "modified": "<ISO8601>"
    },
    "version": "1.0.1",
    "modifier": {
      "id": "string",
      "organization": "string"
    },
    "changes": ["string"]
  }
}
```

### C. Error Handling

1. **Validation Errors**
```json
{
  "error_handling": {
    "timestamp_errors": {
      "invalid_format": {
        "message": "Invalid timestamp format",
        "resolution": "Use ISO 8601 format"
      },
      "future_date": {
        "message": "Timestamp cannot be in future",
        "resolution": "Use current or past date"
      },
      "invalid_sequence": {
        "message": "Invalid timestamp sequence",
        "resolution": "Ensure chronological order"
      }
    },
    "version_errors": {
      "invalid_format": {
        "message": "Invalid version format",
        "resolution": "Use semantic versioning"
      },
      "version_conflict": {
        "message": "Version conflict detected",
        "resolution": "Resolve conflict and retry"
      }
    }
  }
}
```

2. **Resolution Procedures**
```markdown
## Error Resolution Workflow

1. Validation Errors
   - Check format requirements
   - Verify data consistency
   - Update invalid fields
   - Revalidate changes

2. Version Conflicts
   - Identify conflict source
   - Review change history
   - Resolve differences
   - Update version number

3. Access Control Issues
   - Verify permissions
   - Check classification
   - Update access controls
   - Document changes
```

### D. Best Practices

```markdown
## Metadata Management Best Practices

1. Timestamp Management
   - Use consistent timezone (UTC)
   - Regular timestamp validation
   - Automated updates where possible
   - Regular synchronization checks

2. Version Control
   - Clear version numbering
   - Complete change documentation
   - Regular version reviews
   - Proper deprecation handling

3. Information Handling
   - Appropriate TLP marking
   - Regular classification review
   - Clear handling instructions
   - Access control maintenance

4. Quality Control
   - Regular validation checks
   - Comprehensive reviews
   - Documentation updates
   - Audit trail maintenance
```

### E. Migration Guidelines

```markdown
## Metadata Migration Guidelines

1. Preparation
   - Inventory current metadata
   - Map fields to new schema
   - Identify gaps
   - Plan migration strategy

2. Execution
   - Validate source data
   - Transform to new format
   - Verify transformation
   - Update references
   - Document changes

3. Validation
   - Check completeness
   - Verify accuracy
   - Test relationships
   - Validate access controls

4. Documentation
   - Record migration details
   - Update documentation
   - Notify stakeholders
   - Archive old formats

### F. Audit Requirements

```markdown
## Metadata Audit Guidelines

1. Regular Audits
   - Weekly automated checks
   - Monthly manual reviews
   - Quarterly comprehensive audits
   - Annual compliance review

2. Audit Scope
   ```json
   {
     "audit_requirements": {
       "metadata_completeness": {
         "required_fields": [
           "timestamps",
           "version_control",
           "handling_instructions"
         ],
         "validation_rules": [
           "Format compliance",
           "Data consistency",
           "Reference integrity"
         ]
       },
       "access_control": {
         "checks": [
           "Permission validity",
           "Classification accuracy",
           "TLP compliance",
           "Handling adherence"
         ]
       },
       "change_management": {
         "tracking": [
           "Version history",
           "Modification records",
           "Review documentation",
           "Approval chain"
         ]
       }
     }
   }
   ```

3. Audit Documentation
   ```markdown
   ## Audit Report Template

   ### Basic Information
   - Audit Date: [Date]
   - Auditor: [Name]
   - Scope: [Description]

   ### Findings
   1. Completeness Check
      - Required fields: [Status]
      - Optional fields: [Status]
      - Missing data: [Details]

   2. Accuracy Check
      - Data validation: [Status]
      - Reference check: [Status]
      - Consistency: [Status]

   3. Compliance Check
      - TLP compliance: [Status]
      - Access control: [Status]
      - Handling requirements: [Status]

   ### Recommendations
   - [List of recommendations]

   ### Follow-up Actions
   - [Required actions]
   - [Timeline]
   - [Responsible parties]
   ```

### G. Performance Considerations

```json
{
  "performance_guidelines": {
    "metadata_size": {
      "recommended_limit": "10KB",
      "maximum_limit": "50KB",
      "optimization_tips": [
        "Minimize redundant information",
        "Use efficient data structures",
        "Implement pagination for large datasets"
      ]
    },
    "query_optimization": {
      "indexed_fields": [
        "timestamps.modified",
        "version",
        "tlp_marking"
      ],
      "caching_strategy": {
        "cache_duration": "1 hour",
        "cache_invalidation": "On update"
      }
    },
    "update_handling": {
      "batch_processing": {
        "enabled": true,
        "max_batch_size": 1000,
        "processing_interval": "5 minutes"
      },
      "real_time_updates": {
        "enabled": true,
        "max_frequency": "1 per second"
      }
    }
  }
}
```

## Version History

```json
{
  "document_history": {
    "versions": [
      {
        "version": "1.0.0",
        "date": "2023-12-01",
        "author": "STASIS Team",
        "changes": [
          "Initial metadata documentation",
          "Core field definitions",
          "Basic implementation guidelines"
        ]
      },
      {
        "version": "1.0.1",
        "date": "2023-12-15",
        "author": "STASIS Team",
        "changes": [
          "Enhanced audit requirements",
          "Added performance guidelines",
          "Expanded implementation examples"
        ]
      }
    ],
    "planned_updates": [
      {
        "version": "1.1.0",
        "planned_date": "2024-Q1",
        "features": [
          "Advanced metadata validation",
          "Automated quality control",
          "Enhanced audit capabilities",
          "Improved performance optimization",
          "Extended integration options"
        ]
      }
    ]
  }
}
```

## Contact Information

### Support Channels
```json
{
  "support_contacts": {
    "technical_support": {
      "email": "support@stasis.org",
      "hours": "24/7",
      "response_time": "24 hours"
    },
    "documentation": {
      "email": "docs@stasis.org",
      "hours": "Business hours",
      "response_time": "48 hours"
    },
    "security": {
      "email": "security@stasis.org",
      "hours": "24/7",
      "response_time": "4 hours"
    }
  }
}
```

### Community Resources
```json
{
  "community_resources": {
    "github": "https://github.com/stasis-project",
    "documentation": "https://docs.stasis.org",
    "slack": "https://stasis-community.slack.com",
    "mailing_list": "community@stasis.org"
  }
}
```

## Related Documentation

### Core Components
- [Identification](./identification.md)
- [Technical Profile](./technical-profile.md)
- [Behavioral Analysis](./behavioral-analysis.md)
- [Strategic Context](./strategic-context.md)

### Integration Guides
- [API Integration](../integration/api.md)
- [STIX Mapping](../integration/stix.md)
- [MITRE ATT&CK](../integration/attack.md)
- [Custom Integration](../integration/custom.md)

### Best Practices
- [Implementation Guide](../guides/implementation.md)
- [Analysis Methodology](../guides/analysis.md)
- [Quality Control](../guides/quality.md)
- [Security Considerations](../guides/security.md)

## License and Attribution

### License Information
```markdown
Copyright (c) 2023 STASIS Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this documentation except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

### Attribution Requirements
```markdown
## Attribution Guidelines

1. Direct Usage
   - Include copyright notice
   - Maintain license information
   - Provide attribution to STASIS Project

2. Derivative Works
   - Indicate modifications
   - Include original copyright
   - Document changes
   - Maintain license terms

3. Commercial Usage
   - Contact STASIS team
   - Review licensing terms
   - Obtain necessary permissions