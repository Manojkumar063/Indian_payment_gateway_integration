# PhonePe payment handler implementation
import requests
import base64
import json
from .base_payment import BasePaymentHandler

class PhonePePaymentHandler(BasePaymentHandler):
    """PhonePe Payment Gateway Handler"""
    
    def create_payment_request(self, amount: float, customer_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create PhonePe payment request"""
        
        transaction_id = self.generate_transaction_id()
        self.transaction_id = transaction_id
        
        # PhonePe payload
        payload = {
            "merchantId": self.config.PHONEPE_MERCHANT_ID,
            "merchantTransactionId": transaction_id,
            "merchantUserId": customer_info.get('customer_id', f"USER_{transaction_id}"),
            "amount": int(amount * 100),  # Amount in paise
            "redirectUrl": self.config.PHONEPE_CALLBACK_URL,
            "redirectMode": "POST",
            "callbackUrl": self.config.PHONEPE_CALLBACK_URL,
            "mobileNumber": customer_info.get('phone', ''),
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }
        
        # Encode payload
        encoded_payload = base64.b64encode(json.dumps(payload).encode()).decode()
        
        # Generate X-VERIFY header
        string_to_hash = encoded_payload + "/pg/v1/pay" + self.config.PHONEPE_SALT_KEY
        x_verify = self.generate_checksum(string_to_hash, '') + "###" + str(self.config.PHONEPE_SALT_INDEX)
        
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': x_verify
        }
        
        request_data = {
            'request': encoded_payload
        }
        
        try:
            response = requests.post(
                f"{self.config.PHONEPE_HOST_URL}/pg/v1/pay",
                json=request_data,
                headers=headers,
                timeout=10
            )
            
            response_data = response.json()
            
            if response_data.get('success'):
                return {
                    'success': True,
                    'transaction_id': transaction_id,
                    'payment_url': response_data['data']['instrumentResponse']['redirectInfo']['url'],
                    'phonepe_transaction_id': response_data['data']['merchantTransactionId'],
                    'amount': amount,
                    'payment_method': 'PhonePe'
                }
            else:
                return {
                    'success': False,
                    'message': response_data.get('message', 'Payment initiation failed'),
                    'code': response_data.get('code')
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'PhonePe API error: {str(e)}'
            }
    
    def verify_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify PhonePe payment response"""
        
        transaction_id = payment_data.get('transactionId')
        
        if not transaction_id:
            return {
                'success': False,
                'message': 'Transaction ID not found'
            }
        
        # Check transaction status
        status_response = self._check_transaction_status(transaction_id)
        
        return status_response
    
    def _check_transaction_status(self, merchant_transaction_id: str) -> Dict[str, Any]:
        """Check transaction status with PhonePe"""
        
        # Generate X-VERIFY header for status check
        string_to_hash = f"/pg/v1/status/{self.config.PHONEPE_MERCHANT_ID}/{merchant_transaction_id}" + self.config.PHONEPE_SALT_KEY
        x_verify = self.generate_checksum(string_to_hash, '') + "###" + str(self.config.PHONEPE_SALT_INDEX)
        
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': x_verify
        }
        
        try:
            response = requests.get(
                f"{self.config.PHONEPE_HOST_URL}/pg/v1/status/{self.config.PHONEPE_MERCHANT_ID}/{merchant_transaction_id}",
                headers=headers,
                timeout=10
            )
            
            response_data = response.json()
            
            if response_data.get('success'):
                payment_info = response_data.get('data', {})
                return {
                    'success': payment_info.get('state') == 'COMPLETED',
                    'transaction_id': merchant_transaction_id,
                    'phonepe_transaction_id': payment_info.get('transactionId'),
                    'amount': payment_info.get('amount', 0) / 100,  # Convert from paise
                    'status': payment_info.get('state'),
                    'payment_method': payment_info.get('paymentInstrument', {}).get('type'),
                    'response_code': payment_info.get('responseCode'),
                    'message': payment_info.get('responseCodeDescription', 'Payment processed')
                }
            else:
                return {
                    'success': False,
                    'message': response_data.get('message', 'Status check failed'),
                    'code': response_data.get('code')
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'PhonePe status check error: {str(e)}'
            }
