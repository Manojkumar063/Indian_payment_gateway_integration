# Cryptographic utilities for payment integration
import base64
import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class PaytmChecksum:
    """Paytm Checksum utility"""
    
    @staticmethod
    def generateSignature(params, merchant_key):
        """Generate Paytm checksum"""
        data = PaytmChecksum.__getStringByParams(params) + merchant_key
        return PaytmChecksum.__encode(data)
    
    @staticmethod
    def verifySignature(params, merchant_key, checksum):
        """Verify Paytm checksum"""
        data = PaytmChecksum.__getStringByParams(params) + merchant_key
        return PaytmChecksum.__encode(data) == checksum
    
    @staticmethod
    def __encode(data):
        """Encode data"""
        return base64.b64encode(hashlib.sha256(data.encode()).digest()).decode()
    
    @staticmethod
    def __getStringByParams(params):
        """Get string from parameters"""
        data = []
        for key in sorted(params.keys()):
            if key != 'CHECKSUMHASH':
                if params[key] is not None and len(str(params[key])) > 0:
                    data.append(str(params[key]))
        return '|'.join(data) + '|'
