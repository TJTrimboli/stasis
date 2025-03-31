from datetime import datetime
from typing import Dict, Any, Optional
import hashlib
import re

def generate_actor_id(name: str, country_code: str, category: str) -> str:
    """
    Generate a standardized actor ID.
    
    Args:
        name: Actor name
        country_code: ISO 3166-1 alpha-3 country code
        category: Actor category (APT, CRM, HAC)
        
    Returns:
        str: Formatted actor ID
    """
    year = datetime.now().strftime("%y")
    sequence = hashlib.md5(name.encode()).hexdigest()[:3].upper()
    return f"TA{year}{country_code}-{category}{sequence}"

def validate_country_code(code: str) -> bool:
    """Validate ISO 3166-1 alpha-3 country code."""
    return bool(re.match(r'^[A-Z]{3}$', code))

def validate_category(category: str) -> bool:
    """Validate actor category."""
    return category in ['APT', 'CRM', 'HAC']

def calculate_confidence(evidence: Dict[str, Any]) -> int:
    """
    Calculate confidence score based on evidence.
    
    Args:
        evidence: Dictionary containing evidence factors
        
    Returns:
        int: Confidence score (1-5)
    """
    factors = {
        'technical_evidence': 2,
        'behavioral_patterns': 1.5,
        'historical_data': 1,
        'source_reliability': 1.5,
        'correlation_strength': 1
    }
    
    score = 0
    max_score = sum(factors.values())
    
    for factor, weight in factors.items():
        if factor in evidence:
            factor_score = evidence[factor] * weight
            score += factor_score
    
    # Normalize to 1-5 scale
    normalized_score = round((score / max_score) * 4) + 1
    return min(max(normalized_score, 1), 5)

def sanitize_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize input data to prevent injection and ensure proper formatting.
    
    Args:
        data: Dictionary containing input data
        
    Returns:
        Dict[str, Any]: Sanitized data
    """
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Remove potential HTML/script injection
            value = re.sub(r'<[^>]*>', '', value)
            # Remove control characters
            value = ''.join(char for char in value if ord(char) >= 32)
        elif isinstance(value, dict):
            value = sanitize_data(value)
        elif isinstance(value, list):
            value = [sanitize_data(item) if isinstance(item, dict) else item for item in value]
        
        sanitized[key] = value
    
    return sanitized

def merge_actor_data(existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge new actor data with existing data, handling conflicts.
    
    Args:
        existing: Existing actor data
        new: New actor data to merge
        
    Returns:
        Dict[str, Any]: Merged data
    """
    merged = existing.copy()
    
    for key, value in new.items():
        if key not in merged:
            merged[key] = value
        elif isinstance(value, list):
            # Merge lists, removing duplicates
            merged[key] = list(set(merged[key] + value))
        elif isinstance(value, dict):
            merged[key] = merge_actor_data(merged[key], value)
        else:
            # For conflicting values, keep the one with higher confidence
            if new.get('confidence', 0) > existing.get('confidence', 0):
                merged[key] = value
    
    return merged

def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Format timestamp in ISO 8601 format.
    
    Args:
        dt: Datetime object (default: current time)
        
    Returns:
        str: Formatted timestamp
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def parse_timestamp(timestamp: str) -> datetime:
    """
    Parse ISO 8601 timestamp.
    
    Args:
        timestamp: ISO 8601 formatted timestamp string
        
    Returns:
        datetime: Parsed datetime object
    """
    try:
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

def validate_reference_url(url: str) -> bool:
    """
    Validate reference URL format and accessibility.
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if URL is valid and accessible
    """
    import requests
    from urllib.parse import urlparse
    
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
            
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def extract_iocs(text: str) -> Dict[str, list]:
    """
    Extract indicators of compromise from text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dict[str, list]: Dictionary of IOC types and values
    """
    iocs = {
        'ipv4': [],
        'domain': [],
        'url': [],
        'md5': [],
        'sha1': [],
        'sha256': [],
        'email': []
    }
    
    # IPv4 addresses
    ipv4_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    iocs['ipv4'] = re.findall(ipv4_pattern, text)
    
    # Domains
    domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    iocs['domain'] = re.findall(domain_pattern, text)
    
    # URLs
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    iocs['url'] = re.findall(url_pattern, text)
    
    # MD5 hashes
    md5_pattern = r'\b[a-fA-F0-9]{32}\b'
    iocs['md5'] = re.findall(md5_pattern, text)
    
    # SHA1 hashes
    sha1_pattern = r'\b[a-fA-F0-9]{40}\b'
    iocs['sha1'] = re.findall(sha1_pattern, text)
    
    # SHA256 hashes
    sha256_pattern = r'\b[a-fA-F0-9]{64}\b'
    iocs['sha256'] = re.findall(sha256_pattern, text)
    
    # Email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    iocs['email'] = re.findall(email_pattern, text)
    
    return iocs

def validate_tlp_level(tlp: str) -> bool:
    """
    Validate Traffic Light Protocol level.
    
    Args:
        tlp: TLP level to validate
        
    Returns:
        bool: True if valid TLP level
    """
    return tlp.upper() in ['WHITE', 'GREEN', 'AMBER', 'RED']

def generate_reference_id(reference: Dict[str, Any]) -> str:
    """
    Generate a unique reference ID based on content.
    
    Args:
        reference: Reference data dictionary
        
    Returns:
        str: Unique reference ID
    """
    content = f"{reference.get('source', '')}{reference.get('url', '')}{reference.get('date', '')}"
    return f"REF{hashlib.md5(content.encode()).hexdigest()[:8].upper()}"

def validate_confidence_score(score: int) -> bool:
    """
    Validate confidence score range.
    
    Args:
        score: Confidence score to validate
        
    Returns:
        bool: True if valid confidence score
    """
    return isinstance(score, int) and 1 <= score <= 5

class DataValidator:
    """Utility class for data validation functions."""
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: list) -> bool:
        """
        Validate presence of required fields.
        
        Args:
            data: Data dictionary to validate
            required_fields: List of required field names
            
        Returns:
            bool: True if all required fields present
        """
        return all(field in data and data[field] for field in required_fields)

    @staticmethod
    def validate_field_type(value: Any, expected_type: type) -> bool:
        """
        Validate field type.
        
        Args:
            value: Value to validate
            expected_type: Expected type
            
        Returns:
            bool: True if value matches expected type
        """
        return isinstance(value, expected_type)

    @staticmethod
    def validate_field_length(value: str, min_length: int = 0, max_length: int = None) -> bool:
        """
        Validate string field length.
        
        Args:
            value: String to validate
            min_length: Minimum length
            max_length: Maximum length
            
        Returns:
            bool: True if length within bounds
        """
        if not isinstance(value, str):
            return False
        
        length = len(value)
        if length < min_length:
            return False
        if max_length and length > max_length:
            return False
        return True

    @staticmethod
    def validate_enum_value(value: str, valid_values: list) -> bool:
        """
        Validate value against enumerated list.
        
        Args:
            value: Value to validate
            valid_values: List of valid values
            
        Returns:
            bool: True if value in valid_values
        """
        return value in valid_values
