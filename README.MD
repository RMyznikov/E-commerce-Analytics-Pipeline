# E-commerce Analytics Pipeline

Synthetic CSV datasets can be generated with:

```powershell
python -m src.generator.generate_dataset --seed 42
```

By default, files are written to `data/incoming/YYYY-MM-DD/`. Dataset sizes and
the output directory can be changed from the command line:

```powershell
python -m src.generator.generate_dataset `
  --customers 100 `
  --products 30 `
  --orders 250 `
  --order-items 750 `
  --output-dir data/incoming/example
```

Generation order follows the foreign-key dependencies:

1. `customers` and `products`
2. `orders` (depends on customers)
3. `order_items` (depends on orders and products)
4. `payments` (one payment per order; amount is calculated from order items)

Run the tests with:

```powershell
python -m unittest discover -s tests -v
```
