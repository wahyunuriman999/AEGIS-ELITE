# Example — E-commerce Schema

`customers(id, email UNIQUE, created_at)`, `orders(id, customer_id FK, status, created_at)`, `order_items(id, order_id FK, product_id FK, qty, unit_price)`. Foreign keys indexed, `status` uses a lookup table rather than an unconstrained string, and money is stored as an integer (cents) to avoid floating-point rounding errors.
