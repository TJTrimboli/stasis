# Structured Threat Actor Schema & Intelligence System (STASIS) v1.0.0 Documentation

This framework provides a comprehensive, standardized approach to threat actor modeling while maintaining flexibility for various organizational needs and use cases. The JSON schema ensures interoperability, while the implementation guidelines provide clear direction for adoption across different environments.

## Table of Contents

1. Introduction
    - Purpose and Scope
    - Design Principles
    - Benefits
2. Core Concepts
3. Data Model Overview
4. Schema Components
5. Implementation Guide
6. Best Practices
7. Examples
8. Appendices

## 1. Introduction

### Purpose and Scope

Structured Threat Actor Schema & Intelligence System (STASIS) is a standardized framework for documenting, sharing, and analyzing cyber threat actor information. It provides a structured format for representing threat actor characteristics, capabilities, behaviors, and strategic context.

### Design Principles

- Completeness: Comprehensive coverage of threat actor attributes
- Flexibility: Adaptable to various use cases and organizational needs
- Interoperability: Compatible with existing frameworks (STIX, MITRE ATT&CK)
- Scalability: Suitable for both simple and complex implementations
- Consistency: Standardized format for reliable data exchange

### Benefits

- Standardized threat actor profiling
- Improved threat intelligence sharing
- Enhanced analysis capabilities
- Consistent attribution methodology
- Automated processing support
- Clear confidence scoring
- Structured relationship mapping

## 2. Core Concepts

### Threat Actor Identification

The UTAMF implements a standardized identification system using the format: `TA{YY}{XXX}-{CAT}{NUM}`

Components:

- TA: Fixed prefix indicating "Threat Actor"
- YY: Two-digit year of first observation
- XXX: Three-letter geographic origin code (ISO 3166-1)
- CAT: Category code (APT/CRM/HAC)
- NUM: Sequential three-digit number

Example: `TA23CHN-APT001`

### Confidence Scoring

All assessments use a standardized 1-5 confidence scale:

1. Low: Limited evidence, high uncertainty
2. Low-Medium: Some evidence, significant uncertainty
3. Medium: Moderate evidence, reasonable confidence
4. Medium-High: Strong evidence, high confidence
5. High: Extensive evidence, very high confidence

## 3. Data Model Overview

The UTAMF consists of four primary components:

### Core Identification

Contains fundamental identifying information about the threat actor:

- Unique identifier
- Known aliases
- First observed date
- Last active date
- Confidence level

### Technical Profile

Documents technical capabilities and infrastructure:

- Capability assessment
- Tools and malware
- Infrastructure details
- Command and control characteristics
- Exploitation methods

### Behavioral Analysis

Captures patterns and operational characteristics:

- Target sectors
- Geographic focus
- Attack patterns
- MITRE ATT&CK mappings
- Temporal patterns

### Strategic Context

Provides higher-level understanding:

- Motivation
- Strategic goals
- Relationships
- Attribution details
- Resource assessment

## 4. Schema Components

### 4.1 Core Identification

#### 4.1.1 Unique Identifier

```json
"unique_id": {
    "type": "string",
    "pattern": "^TA[0-9]{2}[A-Z]{3}-[A-Z]{3}[0-9]{3}$"
}
```
Required field that follows the standardized naming convention.

#### 4.1.2 Aliases

```json
"aliases": {
    "type": "array",
    "items": {
        "type": "string"
    }
}
```
Alternative names used to identify the threat actor, including:

- Public reporting names
- Internal tracking names
- Common industry references

#### 4.1.3 First Observed

```json
"first_observed": {
    "type": "string",
    "format": "date"
}
```
The earliest confirmed date of activity, formatted as YYYY-MM-DD.

#### 4.1.4 Last Active
```json
"last_active": {
    "type": "string",
    "format": "date"
}
```
The most recent confirmed date of activity, formatted as YYYY-MM-DD. This field should be regularly updated as new activity is observed.

#### 4.1.5 Confidence Level
```json
"confidence_level": {
    "type": "integer",
    "minimum": 1,
    "maximum": 5
}
```
Overall confidence in the threat actor identification and attribution, using the standardized 1-5 scale.

### 4.2 Technical Profile

#### 4.2.1 Capability Level
```json
"capability_level": {
    "type": "string",
    "enum": ["Basic", "Intermediate", "Advanced"]
}
```
Assessment of technical sophistication:
- Basic: Uses publicly available tools, limited custom development
- Intermediate: Mix of public and custom tools, moderate development capabilities
- Advanced: Sophisticated custom tools, significant development capabilities

#### 4.2.2 Tools and Malware
```json
"tools_malware": {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["name", "type"],
        "properties": {
            "name": {
                "type": "string"
            },
            "type": {
                "type": "string",
                "enum": ["RAT", "Backdoor", "Ransomware", "Wiper", "Loader", "Other"]
            },
            "first_seen": {
                "type": "string",
                "format": "date"
            },
            "last_seen": {
                "type": "string",
                "format": "date"
            },
            "variant": {
                "type": "string"
            },
            "hash_values": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    }
}
```
Documentation of known tools and malware:
- name: Identifier for the tool/malware
- type: Classification of the tool's primary function
- first_seen: Initial observation date
- last_seen: Most recent observation date
- variant: Specific version or variant identifier
- hash_values: Associated file hashes

#### 4.2.3 Infrastructure
```json
"infrastructure": {
    "type": "object",
    "properties": {
        "c2_servers": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "hosting_preferences": {
            "type": "string"
        },
        "infrastructure_type": {
            "type": "string",
            "enum": ["Static", "Dynamic", "Hybrid"]
        },
        "known_ip_ranges": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    }
}
```
Infrastructure characteristics:
- c2_servers: Command and control server identifiers
- hosting_preferences: Preferred hosting methods or providers
- infrastructure_type: Classification of infrastructure usage patterns
- known_ip_ranges: Associated IP address ranges

#### 4.2.4 C2 Characteristics
```json
"c2_characteristics": {
    "type": "object",
    "properties": {
        "protocols": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["HTTP", "HTTPS", "DNS", "TCP", "UDP", "ICMP", "Other"]
            }
        },
        "encryption": {
            "type": "string"
        },
        "persistence_method": {
            "type": "string"
        },
        "communication_patterns": {
            "type": "object",
            "properties": {
                "frequency": {
                    "type": "string"
                },
                "beaconing_interval": {
                    "type": "string"
                },
                "data_exfiltration_method": {
                    "type": "string"
                }
            }
        }
    }
}
```
Command and Control (C2) characteristics detail:
- protocols: Communication protocols used for C2
- encryption: Description of encryption methods
- persistence_method: Techniques used to maintain access
- communication_patterns:
  - frequency: How often C2 communication occurs
  - beaconing_interval: Time between check-ins
  - data_exfiltration_method: Methods used to extract data

#### 4.2.5 Exploitation Methods
```json
"exploitation_methods": {
    "type": "array",
    "items": {
        "type": "string"
    }
}
```
Known exploitation techniques and methods used by the threat actor. Should align with MITRE ATT&CK where applicable.

### 4.3 Behavioral Analysis

#### 4.3.1 Target Sectors
```json
"target_sectors": {
    "type": "array",
    "items": {
        "type": "string",
        "enum": [
            "Technology",
            "Defense",
            "Manufacturing",
            "Financial",
            "Healthcare",
            "Government",
            "Energy",
            "Telecommunications",
            "Other"
        ]
    }
}
```
Industries and sectors targeted by the threat actor. Multiple sectors can be specified to indicate broad targeting patterns.

#### 4.3.2 Geographic Focus
```json
"geographic_focus": {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "region": {
                "type": "string"
            },
            "countries": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    }
}
```
Geographic targeting patterns:
- region: Broader geographic area (e.g., "Western Europe", "Southeast Asia")
- countries: Specific countries targeted, using ISO 3166-1 country codes

#### 4.3.3 Attack Patterns
```json
"attack_patterns": {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["technique_id", "technique_name"],
        "properties": {
            "technique_id": {
                "type": "string",
                "pattern": "^T\d{4,}(?:\.\d+)?$"
            },
            "technique_name": {
                "type": "string"
            },
            "sub_techniques": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    }
}
```
MITRE ATT&CK mapping details:
- technique_id: ATT&CK technique identifier
- technique_name: Name of the technique
- sub_techniques: Related sub-techniques

#### 4.3.4 MITRE Mappings
```json
"mitre_mappings": {
    "type": "array",
    "items": {
        "type": "string",
        "enum": [
            "Initial Access",
            "Execution",
            "Persistence",
            "Privilege Escalation",
            "Defense Evasion",
            "Credential Access",
            "Discovery",
            "Lateral Movement",
            "Collection",
            "Command and Control",
            "Exfiltration",
            "Impact"
        ]
    }
}
```
Tactical categories from the MITRE ATT&CK framework that align with the threat actor's observed behaviors.

#### 4.3.5 Time Patterns
```json
"time_patterns": {
    "type": "object",
    "properties": {
        "active_hours": {
            "type": "string"
        },
        "peak_activity": {
            "type": "string"
        },
        "timezone_preference": {
            "type": "string"
        }
    }
}
```
Temporal characteristics:
- active_hours: Primary hours of operation
- peak_activity: Periods of highest activity (e.g., "Monday-Friday")
- timezone_preference: Observed timezone patterns in operations

### 4.4 Strategic Context

#### 4.4.1 Motivation
```json
"motivation": {
    "type": "string",
    "enum": [
        "Cyber Espionage",
        "Financial Gain",
        "Hacktivism",
        "Information Operations",
        "Destructive Attack",
        "Military Advantage",
        "Unknown"
    ]
}
```
Primary assessed motivation for the threat actor's activities. Required field that must match one of the enumerated values.

#### 4.4.2 Goals
```json
"goals": {
    "type": "array",
    "items": {
        "type": "string"
    }
}
```
Specific objectives and aims of the threat actor. May include both tactical and strategic goals.

#### 4.4.3 Relationships
```json
"relationships": {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["group", "relationship_type", "confidence"],
        "properties": {
            "group": {
                "type": "string",
                "pattern": "^TA[0-9]{2}[A-Z]{3}-[A-Z]{3}[0-9]{3}$"
            },
            "relationship_type": {
                "type": "string",
                "enum": [
                    "Shared Infrastructure",
                    "Shared Tools",
                    "Shared TTPs",
                    "Parent Organization",
                    "Subsidiary",
                    "Affiliated",
                    "Competing",
                    "Other"
                ]
            },
            "confidence": {
                "type": "integer",
                "minimum": 1,
                "maximum": 5
            },
            "details": {
                "type": "string"
            }
        }
    }
}
```
Documented relationships with other threat actors:
- group: Identifier of the related threat actor
- relationship_type: Nature of the relationship
- confidence: Confidence in the relationship assessment
- details: Additional context about the relationship

#### 4.4.4 Attribution Confidence
```json
"attribution_confidence": {
    "type": "integer",
    "minimum": 1,
    "maximum": 5
}
```
Overall confidence in the attribution assessment using the standard 1-5 scale.

#### 4.4.5 State Sponsored
```json
"state_sponsored": {
    "type": "object",
    "properties": {
        "assessment": {
            "type": "boolean"
        },
        "suspected_state": {
            "type": "string"
        },
        "confidence": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5
        }
    }
}
```
Assessment of state sponsorship:
- assessment: Boolean indicating suspected state sponsorship
- suspected_state: Name of suspected sponsoring state
- confidence: Confidence in state sponsorship assessment

#### 4.4.6 Resources
```json
"resources": {
    "type": "object",
    "properties": {
        "financial_resources": {
            "type": "string",
            "enum": ["Limited", "Moderate", "Substantial", "Unknown"]
        },
        "personnel_size": {
            "type": "string",
            "enum": ["Individual", "Small Team", "Large Team", "Organization", "Unknown"]
        },
        "technical_resources": {
            "type": "string",
            "enum": ["Limited", "Moderate", "Advanced", "Unknown"]
        }
    }
}
```
Assessment of threat actor resources:
- financial_resources: Level of financial backing
- personnel_size: Estimated size of the organization
- technical_resources: Level of technical capabilities

### 4.5 Metadata

#### 4.5.1 Created and Modified
```json
"created": {
    "type": "string",
    "format": "date-time"
},
"modified": {
    "type": "string",
    "format": "date-time"
}
```
Timestamps for record creation and modification:
- created: Initial creation timestamp (ISO 8601 format)
- modified: Last modification timestamp (ISO 8601 format)

#### 4.5.2 Version
```json
"version": {
    "type": "string"
}
```
Version of the threat actor profile, following semantic versioning (MAJOR.MINOR.PATCH).

#### 4.5.3 Created By and Modified By
```json
"created_by": {
    "type": "string"
},
"modified_by": {
    "type": "string"
}
```
Identifiers for the entities responsible for creating and modifying the record.

#### 4.5.4 References
```json
"references": {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "format": "uri"
            },
            "description": {
                "type": "string"
            },
            "source": {
                "type": "string"
            },
            "date_added": {
                "type": "string",
                "format": "date"
            },
            "confidence": {
                "type": "integer",
                "minimum": 1,
                "maximum": 5
            }
        },
        "required": ["url", "source"]
    }
}
```
Supporting documentation and references:
- url: Link to the reference material
- description: Summary of the reference content
- source: Origin of the reference
- date_added: When the reference was added
- confidence: Confidence in the reference's reliability

#### 4.5.5 Tags
```json
"tags": {
    "type": "array",
    "items": {
        "type": "string"
    }
}
```
Custom labels for categorization and filtering.

#### 4.5.6 TLP Level
```json
"tlp_level": {
    "type": "string",
    "enum": ["WHITE", "GREEN", "AMBER", "RED"]
}
```
Traffic Light Protocol classification for information sharing:
- WHITE: Unlimited disclosure
- GREEN: Community-wide disclosure
- AMBER: Limited disclosure
- RED: Named recipients only

#### 4.5.7 Confidence Justification
```json
"confidence_justification": {
    "type": "string"
}
```
Explanation of the reasoning behind confidence assessments.

## 5. Implementation Guide

### 5.1 Getting Started
1. Review schema requirements
2. Set up JSON validation environment
3. Implement data storage solution
4. Configure API endpoints
5. Establish access controls

### 5.2 Data Entry Guidelines
1. Required Fields
   - unique_id
   - first_observed
   - confidence_level
   - motivation
   - attribution_confidence
   - created
   - modified
   - version

2. Best Practices
   - Use standardized formats for dates and times
   - Maintain consistent naming conventions
   - Regular updates to last_active field
   - Comprehensive documentation of changes
   - Regular validation of data integrity

### 5.3 Data Validation
1. Schema Validation
   - Validate against JSON schema
   - Check required fields
   - Verify enumerated values
   - Validate date formats

2. Content Validation
   - Cross-reference relationships
   - Verify MITRE ATT&CK mappings
   - Check confidence assessments
   - Validate geographic codes

### 5.4 API Integration
1. REST API Endpoints
   - GET /threat-actors
   - GET /threat-actors/{id}
   - POST /threat-actors
   - PUT /threat-actors/{id}
   - DELETE /threat-actors/{id}

2. Authentication
   - API key authentication
   - OAuth 2.0 support
   - Role-based access control

3. Rate Limiting
   - Implement request quotas
   - Define burst limits
   - Set up retry mechanisms

4. Error Handling
   - Standard error codes
   - Detailed error messages
   - Error logging and monitoring

### 5.5 Data Migration
1. Legacy Data Migration
   - Map existing fields to UTAMF schema
   - Transform data formats
   - Validate migrated data
   - Document migration decisions

2. Version Updates
   - Define update procedures
   - Maintain backward compatibility
   - Document schema changes
   - Provide migration scripts

## 6. Best Practices

### 6.1 Data Quality
1. Accuracy
   - Verify information sources
   - Cross-reference data points
   - Regular review cycles
   - Update outdated information

2. Completeness
   - Fill all relevant fields
   - Document unknown values
   - Include supporting evidence
   - Link related entities

3. Consistency
   - Use standardized formats
   - Follow naming conventions
   - Apply consistent confidence scoring
   - Maintain relationship mappings

### 6.2 Information Sharing
1. TLP Guidelines
   - Respect sharing restrictions
   - Mark sensitive data
   - Review before sharing
   - Track distribution

2. Attribution
   - Document sources
   - Maintain chain of evidence
   - Update attribution confidence
   - Note conflicting information

### 6.3 Maintenance
1. Regular Reviews
   - Quarterly assessment
   - Update active status
   - Verify relationships
   - Check reference validity

2. Version Control
   - Track changes
   - Document updates
   - Maintain history
   - Archive old versions

## 7. Examples

### 7.1 Basic Threat Actor Profile
```json
{
    "core_identification": {
        "unique_id": "TA23CHN-APT001",
        "aliases": ["Dragon Force", "APT123"],
        "first_observed": "2023-01-15",
        "last_active": "2023-12-01",
        "confidence_level": 4
    },
    "technical_profile": {
        "capability_level": "Advanced",
        "tools_malware": [
            {
                "name": "DragonRAT",
                "type": "RAT",
                "first_seen": "2023-02-01"
            }
        ]
    }
}
```

### 7.2 Complete Threat Actor Profile
[Detailed example provided in separate documentation due to length]

## 8. Appendices

### 8.1 Confidence Scoring Guidelines
1. Level 1 (Low)
   - Single source
   - Unconfirmed information
   - Historical inconsistencies
   - Limited technical evidence

2. Level 2 (Low-Medium)
   - Multiple sources
   - Some corroboration
   - Limited technical evidence
   - Some historical patterns

3. Level 3 (Medium)
   - Multiple reliable sources
   - Consistent reporting
   - Technical evidence
   - Established patterns

4. Level 4 (Medium-High)
   - Strong corroboration
   - Significant technical evidence
   - Clear patterns
   - Multiple confirmations

5. Level 5 (High)
   - Extensive evidence
   - Multiple reliable sources
   - Strong technical confirmation
   - Clear attribution

### 8.2 Geographic Codes
- Standard ISO 3166-1 alpha-3 country codes
- Regional groupings
- Special designations

### 8.3 Common Tools and Malware Categories
1. Remote Access Tools (RAT)
2. Backdoors
3. Credential Stealers
4. Ransomware
5. Information Stealers
6. Wipers
7. Loaders
8. Custom Malware

### 8.4 MITRE ATT&CK Integration
1. Technique Mapping
2. Sub-technique Usage
3. Procedure Examples
4. Mitigation Strategies

### 8.5 Change Log
- Version 1.0.0 (Initial Release)
  - Base schema implementation
  - Core components defined
  - Basic validation rules
  - Initial documentation

### 8.6 Future Considerations
1. Planned Enhancements
   - Machine learning integration
   - Automated relationship mapping
   - Enhanced visualization capabilities
   - Real-time threat actor tracking
   - Automated confidence scoring

2. Integration Roadmap
   - STIX/TAXII compatibility
   - MISP integration
   - Threat intelligence platform plugins
   - Automated reporting tools
   - API expansion

3. Schema Evolution
   - Additional attribute support
   - Enhanced relationship types
   - Extended metadata fields
   - Custom field support
   - Flexible validation rules

### 8.7 Glossary

#### A
- APT (Advanced Persistent Threat): Sophisticated threat actors with significant resources
- Attribution: Process of identifying threat actors responsible for specific activities

#### B
- Backdoor: Malicious code providing unauthorized access
- Beaconing: Regular communication between malware and control server

#### C
- C2 (Command and Control): Infrastructure used to control malware
- Confidence Level: Degree of certainty in threat intelligence assessment

#### D
- DNS (Domain Name System): Protocol used for domain resolution
- DDoS (Distributed Denial of Service): Attack type disrupting service availability

[Continue through alphabet with relevant terms]

### 8.8 Reference Materials

#### Standards and Frameworks
1. MITRE ATT&CK
   - Enterprise Matrix
   - Mobile Matrix
   - ICS Matrix

2. STIX 2.1
   - Core concepts
   - Implementation guidance
   - Integration patterns

3. ISO Standards
   - ISO 27001
   - ISO 27035
   - ISO 29147

#### Technical References
1. Network Protocols
   - TCP/IP specifications
   - HTTP/HTTPS standards
   - DNS protocol documentation

2. Malware Analysis
   - Static analysis techniques
   - Dynamic analysis methods
   - Network traffic analysis

3. Threat Intelligence
   - Collection methodologies
   - Analysis frameworks
   - Sharing protocols

### 8.9 Support and Community

#### Support Channels
1. Official Support
   - Documentation repository
   - Issue tracking system
   - Technical support email
   - Update notifications

2. Community Resources
   - Discussion forums
   - User groups
   - Implementation guides
   - Code examples

#### Contributing
1. Code Contributions
   - Contribution guidelines
   - Pull request process
   - Code review requirements
   - Testing requirements

2. Documentation Contributions
   - Style guide
   - Review process
   - Translation guidelines
   - Version control

### 8.10 Legal Considerations

#### Compliance
1. Data Protection
   - GDPR compliance
   - Data handling requirements
   - Privacy considerations
   - Data retention policies

2. Information Sharing
   - Legal frameworks
   - Sharing agreements
   - Liability considerations
   - Confidentiality requirements

#### Licensing
1. Framework License
   - Usage terms
   - Distribution rights
   - Attribution requirements
   - Commercial use

2. Third-party Components
   - Dependencies
   - License compatibility
   - Attribution requirements
   - Usage restrictions

### 8.11 Implementation Checklist

#### Planning Phase
1. Requirements Analysis
   - [ ] Identify use cases
   - [ ] Define success criteria
   - [ ] Assess technical requirements
   - [ ] Review compliance needs

2. Resource Planning
   - [ ] Identify team members
   - [ ] Allocate budget
   - [ ] Schedule milestones
   - [ ] Plan training

#### Implementation Phase
1. Technical Setup
   - [ ] Install dependencies
   - [ ] Configure environment
   - [ ] Set up databases
   - [ ] Configure APIs

2. Data Migration
   - [ ] Map existing data
   - [ ] Validate conversion
   - [ ] Perform migration
   - [ ] Verify results

#### Validation Phase
1. Testing
   - [ ] Unit tests
   - [ ] Integration tests
   - [ ] Performance tests
   - [ ] Security tests

2. Documentation
   - [ ] User guides
   - [ ] API documentation
   - [ ] Maintenance procedures
   - [ ] Training materials