const express = require('express');
const conekta = require('conekta');

const port = 9292;
const yourDomain = 'http://localhost:9292';

const app = express();

// Use your private API key
conekta.api_key = 'key_xxxxxxxxxxx';
conekta.locale = 'es';

app.use(express.static('public'));

app.get('/', (_, res) => {
  res.send('Hello World!')
})

app.post('/create-checkout', async (_, res) => {
  try {
    const customer = await conekta.Customer.create({
      name: 'New Customer',
      email: 'new@customer.com'
    });
  
    const order = await conekta.Order.create({
      currency: 'MXN',
      customer_info: {
        customer_id: customer._id
      },
      line_items: [
        {
          name: 'T-Rex',
          unit_price: 10000,
          quantity: 1
        }
      ],
      checkout: {
        type: 'HostedPayment',
        name: 'Checkout Dummy',
        allowed_payment_methods: ['cash', 'card', 'bank_transfer'],
        success_url: yourDomain + '/success.html',
        failure_url: yourDomain + '/cancel.html',
      }
    })

    const orderObject = order.toObject();

    res.redirect(303, orderObject.checkout.url);
  } catch(e) {
    console.log(e);
  }  
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
