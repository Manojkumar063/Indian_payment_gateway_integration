# Base class for payment handlers
from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
import hashlib
import hmac
import base64
import json

class BasePaymentHandler(ABC):
    """Abstract base class for payment handlers"""
    
    def __init__(self, config):
        self.config = config
        self.transaction_id = None
    
    @abstractmethod
    def create_payment_request(self, amount: float, customer_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create payment request"""
        pass
    
    @abstractmethod
    def verify_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify payment response"""
        pass
    
    def generate_transaction_id(self) -> str:
        """Generate unique transaction ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"TXN_{timestamp}_{hash(datetime.now().microsecond) % 10000:04d}"
    
    def generate_checksum(self, data: str, key: str) -> str:
        """Generate checksum for payment verification"""
        return base64.b64encode(
            hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).digest()
        ).decode('utf-8')
    
    def verify_checksum(self, data: str, checksum: str, key: str) -> bool:
        """Verify checksum"""
        generated_checksum = self.generate_checksum(data, key)
        return generated_checksum == checksum
