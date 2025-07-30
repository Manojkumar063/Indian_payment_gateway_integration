# Entry point for the payment integration application
from flask import Flask, request, render_template, jsonify, redirect
import json

from config.settings import config
from payment_gateways.upi_handler import UPIPaymentHandler
from payment_gateways.paytm_handler import PaytmPaymentHandler
from payment_gateways.phonepe_handler import PhonePePaymentHandler
from payment_gateways.googlepay_handler import GooglePayHandler

app = Flask(__name__)

# Initialize payment handlers
upi_handler = UPIPaymentHandler(config)
paytm_handler = PaytmPaymentHandler(config)
phonepe_handler = PhonePePaymentHandler(config)
googlepay_handler = GooglePayHandler(config)

@app.route('/')
def index():
    """Main payment page"""
    return render_template('payment_page.html')

@app.route('/api/payment/initiate', methods=['POST'])
def initiate_payment():
    """Initiate payment with selected method"""
    
    data = request.get_json()
    payment_method = data.get('payment_method')
    amount = float(data.get('amount'))
    customer_info = data.get('customer_info', {})
    
    try:
        if payment_method == 'upi':
            result = upi_handler.create_payment_request(amount, customer_info)
        elif payment_method == 'paytm':
            result = paytm_handler.create_payment_request(amount, customer_info)
        elif payment_method == 'phonepe':
            result = phonepe_handler.create_payment_request(amount, customer_info)
        elif payment_method == 'googlepay':
            result = googlepay_handler.create_payment_request(amount, customer_info)
        else:
            return jsonify({'success': False, 'message': 'Invalid payment method'})
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/paytm/callback', methods=['POST'])
def paytm_callback():
    """Paytm payment callback"""
    
    payment_data = request.form.to_dict()
    result = paytm_handler.verify_payment(payment_data)
    
    # Store result in database and redirect user
    if result['success']:
        return render_template('payment_success.html', data=result)
    else:
        return render_template('payment_failed.html', data=result)

@app.route('/phonepe/callback', methods=['POST'])
def phonepe_callback():
    """PhonePe payment callback"""
    
    payment_data = request.get_json() or request.form.to_dict()
    result = phonepe_handler.verify_payment(payment_data)
    
    if result['success']:
        return render_template('payment_success.html', data=result)
    else:
        return render_template('payment_failed.html', data=result)

@app.route('/googlepay/process', methods=['POST'])
def googlepay_process():
    """Process Google Pay payment"""
    
    payment_data = request.get_json()
    result = googlepay_handler.verify_payment(payment_data)
    
    return jsonify(result)

@app.route('/api/payment/status/<transaction_id>', methods=['GET'])
def check_payment_status(transaction_id):
    """Check payment status"""
    
    payment_method = request.args.get('method')
    
    try:
        if payment_method == 'paytm':
            result = paytm_handler._check_transaction_status(transaction_id)
        elif payment_method == 'phonepe':
            result = phonepe_handler._check_transaction_status(transaction_id)
        else:
            result = {'success': False, 'message': 'Status check not available for this payment method'}
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
