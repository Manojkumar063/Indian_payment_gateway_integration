# UPI payment handler implementation
import qrcode
from io import BytesIO
import base64
from urllib.parse import quote
from .base_payment import BasePaymentHandler

class UPIPaymentHandler(BasePaymentHandler):
    """UPI Payment Handler for direct UPI integration"""
    
    def create_payment_request(self, amount: float, customer_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create UPI payment request with QR code"""
        
        transaction_id = self.generate_transaction_id()
        self.transaction_id = transaction_id
        
        # UPI URL format
        upi_url = self._generate_upi_url(amount, customer_info, transaction_id)
        
        # Generate QR Code
        qr_code_data = self._generate_qr_code(upi_url)
        
        # Deep links for specific apps
        deep_links = self._generate_deep_links(upi_url)
        
        return {
            'success': True,
            'transaction_id': transaction_id,
            'upi_url': upi_url,
            'qr_code': qr_code_data,
            'deep_links': deep_links,
            'amount': amount,
            'payment_method': 'UPI'
        }
    
    def _generate_upi_url(self, amount: float, customer_info: Dict[str, Any], transaction_id: str) -> str:
        """Generate UPI URL"""
        params = {
            'pa': self.config.UPI_VPA,  # Payee Address
            'pn': quote(self.config.UPI_MERCHANT_NAME),  # Payee Name
            'mc': self.config.UPI_MERCHANT_CODE,  # Merchant Code
            'tr': transaction_id,  # Transaction Reference
            'tn': quote(f"Payment for Order {transaction_id}"),  # Transaction Note
            'am': str(amount),  # Amount
            'cu': 'INR',  # Currency
        }
        
        # Add customer phone if available
        if customer_info.get('phone'):
            params['pn'] = quote(f"{self.config.UPI_MERCHANT_NAME} - {customer_info['phone']}")
        
        # Build UPI URL
        upi_params = '&'.join([f"{key}={value}" for key, value in params.items()])
        return f"upi://pay?{upi_params}"
    
    def _generate_qr_code(self, upi_url: str) -> str:
        """Generate QR code for UPI URL"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(upi_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_data = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_data}"
    
    def _generate_deep_links(self, upi_url: str) -> Dict[str, str]:
        """Generate deep links for specific UPI apps"""
        base_params = upi_url.replace('upi://pay?', '')
        
        return {
            'google_pay': f"tez://upi/pay?{base_params}",
            'phonepe': f"phonepe://pay?{base_params}",
            'paytm': f"paytmmp://pay?{base_params}",
            'bhim': f"bhim://pay?{base_params}",
            'amazon_pay': f"amazonpay://pay?{base_params}",
            'generic': upi_url
        }
    
    def verify_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify UPI payment (usually done via webhook or status check API)"""
        # This would typically involve checking with your payment gateway
        # For UPI direct integration, you'd need to implement status checking
        
        return {
            'success': True,
            'transaction_id': payment_data.get('transaction_id'),
            'status': 'pending',  # pending, success, failed
            'message': 'Payment verification requires manual checking or webhook integration'
        }
