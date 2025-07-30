# Configuration settings for payment integration
import os
from dataclasses import dataclass

@dataclass
class PaymentConfig:
    """Payment Gateway Configuration"""
    
    # Paytm Configuration
    PAYTM_MERCHANT_ID = os.getenv('PAYTM_MERCHANT_ID', 'your_merchant_id')
    PAYTM_MERCHANT_KEY = os.getenv('PAYTM_MERCHANT_KEY', 'your_merchant_key')
    PAYTM_WEBSITE = os.getenv('PAYTM_WEBSITE', 'WEBSTAGING')
    PAYTM_CHANNEL_ID = os.getenv('PAYTM_CHANNEL_ID', 'WEB')
    PAYTM_INDUSTRY_TYPE = os.getenv('PAYTM_INDUSTRY_TYPE', 'Retail')
    PAYTM_CALLBACK_URL = os.getenv('PAYTM_CALLBACK_URL', 'http://localhost:5000/paytm/callback')
    
    # PhonePe Configuration
    PHONEPE_MERCHANT_ID = os.getenv('PHONEPE_MERCHANT_ID', 'your_phonepe_merchant_id')
    PHONEPE_SALT_KEY = os.getenv('PHONEPE_SALT_KEY', 'your_phonepe_salt_key')
    PHONEPE_SALT_INDEX = int(os.getenv('PHONEPE_SALT_INDEX', '1'))
    PHONEPE_HOST_URL = os.getenv('PHONEPE_HOST_URL', 'https://api-preprod.phonepe.com/apis/pg-sandbox')
    PHONEPE_CALLBACK_URL = os.getenv('PHONEPE_CALLBACK_URL', 'http://localhost:5000/phonepe/callback')
    
    # Google Pay Configuration  
    GOOGLEPAY_ENVIRONMENT = os.getenv('GOOGLEPAY_ENVIRONMENT', 'TEST')
    GOOGLEPAY_MERCHANT_ID = os.getenv('GOOGLEPAY_MERCHANT_ID', 'your_google_merchant_id')
    GOOGLEPAY_GATEWAY = os.getenv('GOOGLEPAY_GATEWAY', 'example')
    GOOGLEPAY_GATEWAY_MERCHANT_ID = os.getenv('GOOGLEPAY_GATEWAY_MERCHANT_ID', 'your_gateway_merchant_id')
    
    # UPI Configuration
    UPI_VPA = os.getenv('UPI_VPA', 'merchant@upi')
    UPI_MERCHANT_NAME = os.getenv('UPI_MERCHANT_NAME', 'Merchant Name')
    UPI_MERCHANT_CODE = os.getenv('UPI_MERCHANT_CODE', '1234')

config = PaymentConfig()
