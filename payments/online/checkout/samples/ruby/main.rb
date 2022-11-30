require 'conekta'
require 'sinatra'

# Entra a Panel (panel.conekta.com) para obtener tus api keys
Conekta.api_key = 'key_xxxxxxx'

set :static, true
set :port, 9292

YOUR_DOMAIN = 'http://localhost:4242'.freeze

post '/create-checkout' do
  customer = Conekta::Customer.create(
    {
      name: 'Matz',
      email: 'matz@rules.com'
    }
  )

  order_params =
    {
      currency: 'MXN',
      customer_info: {
        customer_id: customer.id
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
        allowed_payment_methods: %w[cash card bank_transfer],
        success_url: YOUR_DOMAIN + '/success.html',
        failure_url: YOUR_DOMAIN + '/cancel.html',
      }
    }

  order = Conekta::Order.create(order_params)

  redirect order.checkout.url, 303
end
