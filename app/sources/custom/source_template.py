from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
import logging as logger

class CustomSource(ABC):
    """Base class for implementing custom threat actor data sources."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__
        self.last_update = None

    @abstractmethod
    async def fetch_data(self) -> List[Dict[str, Any]]:
        """Fetch threat actor data from the source."""
        pass

    @abstractmethod
    async def parse_data(self, raw_data: Any) -> List[Dict[str, Any]]:
        """Parse raw data into standardized format."""
        pass

    @abstractmethod
    def validate_data(self, parsed_data: List[Dict[str, Any]]) -> bool:
        """Validate parsed data against schema."""
        pass

    async def update(self) -> List[Dict[str, Any]]:
        """Update threat actor data from this source."""
        try:
            raw_data = await self.fetch_data()
            parsed_data = await self.parse_data(raw_data)
            
            if self.validate_data(parsed_data):
                self.last_update = datetime.now()
                return parsed_data
            return []
            
        except Exception as e:
            logger.error(f"Error updating from {self.name}: {str(e)}")
            return []