CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.customers
(
    customer_id  VARCHAR PRIMARY KEY,
    first_name   VARCHAR,
    last_name    VARCHAR,
    email        VARCHAR,
    country      CHAR(2),
    created_at   TIMESTAMPTZ,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.products
(
    product_id   VARCHAR PRIMARY KEY,
    name         VARCHAR,
    category     VARCHAR,
    unit_price   NUMERIC(12, 2),
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.orders
(
    order_id     VARCHAR PRIMARY KEY,
    ordered_at   TIMESTAMPTZ,
    status       VARCHAR,
    customer_id  VARCHAR REFERENCES raw.customers (customer_id),
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.order_items
(
    order_item_id VARCHAR PRIMARY KEY,
    quantity      INTEGER,
    product_id    VARCHAR REFERENCES raw.products (product_id),
    order_id      VARCHAR REFERENCES raw.orders (order_id),
    processed_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.payments
(
    payment_id     VARCHAR PRIMARY KEY,
    order_id       VARCHAR REFERENCES raw.orders (order_id),
    payment_method VARCHAR,
    amount         NUMERIC(12, 2),
    payment_status VARCHAR,
    paid_at        TIMESTAMPTZ,
    processed_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
