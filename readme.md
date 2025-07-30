# Payment Gateway Integration Demo

A professional, responsive payment gateway integration demo showcasing Indian payment methods including UPI, digital wallets, and traditional payment options.
<img width="935" height="902" alt="image" src="https://github.com/user-attachments/assets/21351c14-4b8c-4f83-a1f3-c9d48d667a23" />

## 🚀 Features

- **Multiple Payment Methods**: UPI, Paytm, PhonePe, Google Pay, Cards & Net Banking
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Validation**: Form validation for amount, phone, and email
- **Interactive UI**: Smooth animations and hover effects
- **Payment Simulation**: Realistic payment flow simulation with success/failure scenarios
- **Professional Design**: Clean, corporate-ready interface

## 💳 Supported Payment Methods

1. **UPI Payment** - Universal payment interface for all UPI apps
2. **Paytm** - Wallet, UPI, Cards, Net Banking
3. **PhonePe** - Wallet, UPI, Cards
4. **Google Pay** - UPI and saved payment methods
5. **Cards & Net Banking** - Credit/Debit cards, Net Banking, EMI

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with modern design patterns
- **Responsive**: CSS Grid and Flexbox
- **No Dependencies**: Pure vanilla implementation

## 📁 Project Structure

```
payment-gateway-demo/
├── index.html          # Main application file
├── css/
│   └── styles.css      # Stylesheet (optional - can be external)
├── js/
│   └── script.js       # JavaScript (optional - can be external)
├── assets/
│   └── screenshots/    # Demo screenshots
├── README.md           # Project documentation
└── LICENSE             # License file
```

## 🚀 Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, Edge)
- No server setup required - runs directly in browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/payment-gateway-demo.git
   cd payment-gateway-demo
   ```

2. **Open in browser**
   ```bash
   # Simply open index.html in your browser
   # Or serve locally using:
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

3. **Or use Live Server (VS Code)**
   - Install Live Server extension
   - Right-click on `index.html`
   - Select "Open with Live Server"

## 💻 Usage

1. **Enter Payment Details**
   - Amount (required)
   - Mobile number (optional, 10 digits)
   - Email address (optional)

2. **Select Payment Method**
   - Click on any payment method card
   - Follow the simulated payment flow

3. **Complete Payment**
   - Payment will be simulated automatically
   - Success/failure scenarios are randomly generated
   - Transaction ID is generated for each payment

## 🎨 Customization

### Colors
Update the CSS custom properties in `styles.css`:
```css
:root {
  --primary-color: #1e293b;
  --secondary-color: #475569;
  --background-color: #f8fafc;
  --success-color: #059669;
  --warning-color: #d97706;
}
```

### Payment Methods
Add new payment methods in the HTML and corresponding JavaScript handlers:
```javascript
function initiatePayment(method) {
  // Add your payment method logic here
}
```

## 🔧 API Integration

To integrate with real payment gateways:

1. **Replace mock functions** with actual API calls
2. **Add API keys** (use environment variables)
3. **Implement webhooks** for payment status updates
4. **Add proper error handling** for network failures
5. **Implement security measures** (HTTPS, input sanitization)

### Example API Integration
```javascript
async function initiatePayment(method) {
  try {
    const response = await fetch('/api/payment/initiate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify(paymentData)
    });
    
    const result = await response.json();
    handlePaymentResponse(method, result);
  } catch (error) {
    console.error('Payment error:', error);
  }
}
```

## 🔒 Security Considerations

- **Input Validation**: All user inputs are validated
- **XSS Protection**: HTML is properly escaped
- **HTTPS Required**: Always use HTTPS in production
- **API Security**: Implement proper authentication
- **PCI Compliance**: Follow PCI DSS guidelines for card data

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you have any questions or issues:

- Create an [Issue](https://github.com/yourusername/payment-gateway-demo/issues)
- Email: your.email@example.com
- Documentation: [Wiki](https://github.com/yourusername/payment-gateway-demo/wiki)

## 🙏 Acknowledgments

- Design inspiration from modern payment interfaces
- Icons and animations from CSS libraries
- Indian payment ecosystem guidelines

## 📊 Demo

Try the live demo: [Payment Gateway Demo](https://yourusername.github.io/payment-gateway-demo)

### Screenshots

![Payment Methods](assets/screenshots/payment-methods.png)
![UPI Payment](assets/screenshots/upi-payment.png)
![Payment Success](assets/screenshots/payment-success.png)

---

**Note**: This is a demonstration project. For production use, integrate with actual payment gateway APIs and implement proper security measures.
