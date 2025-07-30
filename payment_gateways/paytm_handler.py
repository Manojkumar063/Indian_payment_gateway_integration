# Paytm payment handler implementation
import requests
import json
from .base_payment import BasePaymentHandler
from utils.crypto_utils import PaytmChecksum

class PaytmPaymentHandler(BasePaymentHandler):
    """Paytm Payment Gateway Handler"""
    
    def create_payment_request(self, amount: float, customer_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create Paytm payment request"""
        
        transaction_id = self.generate_transaction_id()
        self.transaction_id = transaction_id
        
        # Paytm payment parameters
        paytm_params = {
            'MID': self.config.PAYTM_MERCHANT_ID,
            'WEBSITE': self.config.PAYTM_WEBSITE,
            'CHANNEL_ID': self.config.PAYTM_CHANNEL_ID,
            'INDUSTRY_TYPE_ID': self.config.PAYTM_INDUSTRY_TYPE,
            'ORDER_ID': transaction_id,
            'CUST_ID': customer_info.get('customer_id', f"CUST_{transaction_id}"),
            'TXN_AMOUNT': str(amount),
            'CALLBACK_URL': self.config.PAYTM_CALLBACK_URL,
        }
        
        # Add optional customer details
        if customer_info.get('email'):
            paytm_params['EMAIL'] = customer_info['email']
        if customer_info.get('phone'):
            paytm_params['MOBILE_NO'] = customer_info['phone']
        
        # Generate checksum
        checksum = PaytmChecksum.generateSignature(paytm_params, self.config.PAYTM_MERCHANT_KEY)
        paytm_params['CHECKSUMHASH'] = checksum
        
        return {
            'success': True,
            'transaction_id': transaction_id,
            'payment_url': 'https://securegw-stage.paytm.in/theia/processTransaction',
            'form_data': paytm_params,
            'amount': amount,
            'payment_method': 'Paytm'
        }
    
    def verify_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify Paytm payment response"""
        
        # Extract checksum
        received_checksum = payment_data.pop('CHECKSUMHASH', '')
        
        # Verify checksum
        is_valid = PaytmChecksum.verifySignature(
            payment_data, 
            self.config.PAYTM_MERCHANT_KEY, 
            received_checksum
        )
        
        if not is_valid:
            return {
                'success': False,
                'message': 'Invalid checksum',
                'status': 'failed'
            }
        
        # Check transaction status with Paytm
        status_response = self._check_transaction_status(payment_data['ORDERID'])
        
        return {
            'success': payment_data.get('STATUS') == 'TXN_SUCCESS',
            'transaction_id': payment_data.get('ORDERID'),
            'paytm_txn_id': payment_data.get('TXNID'),
            'amount': payment_data.get('TXNAMOUNT'),
            'status': payment_data.get('STATUS'),
            'message': payment_data.get('RESPMSG'),
            'bank_name': payment_data.get('BANKNAME'),
            'payment_mode': payment_data.get('PAYMENTMODE'),
            'verification': status_response
        }
    
    def _check_transaction_status(self, order_id: str) -> Dict[str, Any]:
        """Check transaction status with Paytm"""
        
        status_params = {
            'MID': self.config.PAYTM_MERCHANT_ID,
            'ORDERID': order_id
        }
        
        checksum = PaytmChecksum.generateSignature(
            status_params, 
            self.config.PAYTM_MERCHANT_KEY
        )
        status_params['CHECKSUMHASH'] = checksum
        
        try:
            response = requests.post(
                'https://securegw-stage.paytm.in/merchant-status/getTxnStatus',
                json=status_params,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}
