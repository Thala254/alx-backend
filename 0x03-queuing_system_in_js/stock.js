import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const listProducts = [
  {
    id: 1,
    name: 'Suitcase 250',
    price: 50,
    stock: 4,
  },
  {
    id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10,
  },
  {
    id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2,
  },
  {
    id: 4,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5,
  },
];

const products = listProducts.map((product) => ({
  itemId: product.id,
  itemName: product.name,
  price: product.price,
  initialAvailableQuantity: product.stock,
}));

const getItemById = (id) => products.find((product) => product.itemId === id);

const app = express();
const client = createClient();

const reserveStockById = async (itemId, stock) => promisify(client.set).bind(client)(`item.${itemId}`, stock);

const getCurrentReservedStockById = async (itemId) => promisify(client.get).bind(client)(`item.${itemId}`);

app.get('/list_products', (_, res) => res.json(products));

app.get('/list_products/:itemId', async (req, res) => {
  const item = getItemById(parseInt(req.params.itemId, 10));
  if (!item) res.json({ status: 'Product not found' });
  res.json({
    ...item,
    currentQuantity: item.initialAvailableQuantity
      - parseInt(await getCurrentReservedStockById(item.itemId) || 0, 10),
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const item = getItemById(parseInt(req.params.itemId, 10));
  if (!item) res.json({ status: 'Product not found' });
  if (await getCurrentReservedStockById(item.itemId) >= item.initialAvailableQuantity) {
    res.json({
      status: 'Not enough stock available',
      itemId: parseInt(req.params.itemId, 10),
    });
    return;
  }
  const reserved = parseInt(await getCurrentReservedStockById(item.itemId), 10) || 0;
  await reserveStockById(item.itemId, reserved + 1);
  item.currentQuantity = item.initialAvailableQuantity
    - await getCurrentReservedStockById(item.itemId);
  res.json({
    status: 'Reservation confirmed',
    itemId: item.itemId,
  });
});

const resetProductsStock = async () => products.forEach((product) => promisify(client.set).bind(client)(`item.${product.itemId}`, 0));

app.listen(1245, async () => {
  await resetProductsStock();
  console.log('Server listening at port 1245');
});

export default app;
