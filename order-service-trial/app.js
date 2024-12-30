const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.json());

// MongoDB Connection
mongoose.connect('mongodb://mongodb:27017/orders', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

// Order Schema
const OrderSchema = new mongoose.Schema({
    customer_id: Number,
    product: String,
    quantity: Number
});

const Order = mongoose.model('Order', OrderSchema);

app.post('/order', async (req, res) => {
    const order = new Order(req.body);
    await order.save();
    res.status(201).send({ status: 'Order created' });
});

app.get('/order/:id', async (req, res) => {
    const order = await Order.findById(req.params.id);
    res.send(order);
});

app.listen(5002, () => {
    console.log('Order service is running on port 5002');
});
