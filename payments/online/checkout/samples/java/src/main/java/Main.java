import conekta.io.client.impl.CustomersClient;
import conekta.io.client.impl.OrdersClient;
import conekta.io.config.ConektaAuthenticator;
import conekta.io.model.impl.Customer;
import conekta.io.model.impl.Order;
import conekta.io.model.request.CustomerReq;
import conekta.io.model.request.OrderReq;
import conekta.io.model.submodel.LineItem;

import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static spark.Spark.*;

public class Main {
    public static void main(String[] args) {
        port(9292);
        staticFiles.externalLocation(
                Paths.get("public").toAbsolutePath().toString());
        ConektaAuthenticator.getInstance();
        ConektaAuthenticator.setCredentials("key_sOouZsGD76D896uwt8mbLX0", "");


        post("/create-checkout", (request, response) -> {
            String YOUR_DOMAIN = "http://localhost:9292";

            Customer customer = createCustomer();
            CustomerReq customerInfo = new CustomerReq();
            customerInfo.setCustomerId(customer.getId());

            LineItem lineItem = new LineItem();
            lineItem.setName("T-Rex");
            lineItem.setUnitPrice(10000);
            lineItem.setQuantity(1);

            List<LineItem> lineItems = new ArrayList<>();
            lineItems.add(lineItem);

            conekta.io.model.submodel.Checkout checkout = new conekta.io.model.submodel.Checkout();
            checkout.setType("HostedPayment");
            checkout.setName("Checkout Dummy");
            checkout.setAllowedPaymentMethods(Arrays.asList(new String[]{"card", "cash", "bank_transfer"}));
            checkout.setSuccessUrl(YOUR_DOMAIN + "/success.html");
            checkout.setFailureUrl(YOUR_DOMAIN + "/cancel.html");

            OrderReq orderReq = new OrderReq();
            orderReq.setCurrency("MXN");
            orderReq.setCustomerInfo(customerInfo);
            orderReq.setLineItems(lineItems);
            orderReq.setCheckout(checkout);

            OrdersClient ordersClient = new OrdersClient();
            var OrderResponse = ordersClient.createOrder(orderReq);
            Order order = OrderResponse.getData();;
            response.redirect(order.getCheckout().getUrl(), 303);
            return "";
        });
    }

    private static Customer createCustomer(){
        CustomerReq customerReq = new CustomerReq();
        customerReq.setName("New Customer");
        customerReq.setEmail("new@customer.com");
        CustomersClient customersClient = new CustomersClient();
        return customersClient.createCustomer(customerReq).getData();
    }
}
