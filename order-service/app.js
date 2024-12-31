const express = require('express');
const mongoose = require('mongoose');
// const axios = require('axios');
const dapr = require('@dapr/dapr');
const client1 = require('prom-client');
const daprHost = 'http://localhost'; // Dapr Sidecar Host (not used for Axios)
const daprPort = '3500'; // Dapr HTTP Port (not used for Axios)
const STATE_STORE_NAME = 'mongodb-state-store'; // State store component name
const client = new dapr.DaprClient(daprHost, daprPort); // Dapr Client

const app = express();
app.use(express.json());

// MongoDB Connection
mongoose.connect('mongodb://mongodb-service:27017/order_db', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

// Order Schema
const OrderSchema = new mongoose.Schema({
    order_id: Number,
    customer_id: Number,
    product_id: Number,
    quantity: Number
});

const Order = mongoose.model('Order', OrderSchema);


const register = new client1.Registry();

// Collecte les métriques par défaut (CPU, mémoire, etc.)
client1.collectDefaultMetrics({ register });

// Create a new order and call Customer and Product services
app.post('/order', async (req, res) => {
    const order = new Order(req.body);

    try {
        // // 1. Call Customer service to check if the customer exists
        // const customer = await axios.get(`http://localhost:3500/v1.0/invoke/customer-service/method/customer/get/${order.customer_id}`);
        // if (customer == null) {
        //     return res.status(404).send({ error: 'Customer not found' });
        // }

        // console.log('Customer:', customer);
        // console.log('Customer Data:', customer.data);

        // // 2. Call Product service to validate product availability
        // const product = await axios.get(`http://localhost:3500/v1.0/invoke/product-service/method/product/get/${order.product_id}`);
        // if (product.stock < order.quantity) {
        //     return res.status(400).send({ error: 'Ordered quantity exceeds available stock' });
        // }

        // console.log('Product:', product);
        // console.log('Product Data:', product.data);

        // Save the order
        await order.save();

        // Save to Dapr State Store
        const stateData = [
            {
                key: `order-${order.order_id}`,
                value: order
            }
        ];

        await client.state.save(STATE_STORE_NAME, stateData);

        // const updatedStock = product.stock - order.quantity;

        // // Invoke Product Service to update stock
        // await axios.put(`http://localhost:3500/v1.0/invoke/product-service/product/update/${order.product_id}`, {
        //     name: product.name,
        //     price: product.price,
        //     stock: updatedStock
        // });

        res.status(201).send({
            status: 'Order created',
            order: order,
            // customerService: customer.data,
            // productService: product.data
        });
    } catch (error) {
        console.error('Error creating order:', error);
        res.status(500).send({ error: 'Failed to create order' });
    }
});

// Get order by ID
app.get('/order/:id', async (req, res) => {
    const orderId = req.params.id;

    try {
        const order = await client.state.get(STATE_STORE_NAME, `order-${orderId}`);
        if (order == null) {
            res.status(404).send({ error: 'Order not found' });
        } else {
            res.status(200).send(order);
        }
    } catch (error) {
        console.error('Error getting order:', error);
        res.status(500).send({ error: 'Failed to get order' });
    }
});


// Endpoint pour exposer vos métriques
app.get('/metrics', async (req, res) => {
    res.setHeader('Content-Type', register.contentType);
    res.send(await register.metrics());
  });
 
  
app.listen(5002, () => {
    console.log('Order service is running on port 5002');
});
