# Phase 5 — Gold

**Branch:** `phase-5-gold`

## Goal

Model the Silver tables into a business-ready star schema that's easy for Genie, dashboards, and analysts to query.

## What you'll learn

- Fact vs dimension tables; grain of a fact table (`fact_orders` — one row per order item, or per order? decide and justify).
- Point-in-time joins against SCD2 dimensions (joining a fact to the dimension row that was valid *at the time of the order*, not the current row).
- Materialized views (`mv_<metric>`) vs plain Gold tables — when the extra maintenance is worth it.
- Table/column comments — required for Genie (Phase 8) to answer questions accurately.

## Olist entities/tables involved

`slv_orders`, `slv_order_items`, `slv_payments`, `slv_reviews`, `dim_customer` (SCD2), `dim_product` (SCD1), plus a new `dim_seller` (Olist's real sellers + geolocation tables — a dimension ShopStream-style projects don't usually have) and `dim_date`.

## Steps

- [ ] Build `dim_date` (standard calendar dimension, generated, not sourced from Olist).
- [ ] Build `dim_seller` from `olist_sellers_dataset` + `olist_geolocation_dataset`.
- [ ] Build `fact_orders` joining orders/items/payments/reviews at your chosen grain, with point-in-time keys into `dim_customer` and `dim_product`.
- [ ] Add table and column comments to every Gold object.
- [ ] Build one materialized view (e.g. `mv_daily_sales_by_state`) and explain why it's a materialized view rather than a plain query.

## Done criteria

- `fact_orders` joins cleanly to all four dimensions with no fan-out bugs (row counts match expectations).
- A point-in-time join against `dim_customer` returns the customer's tier *as of the order date*, not today's tier.
- Every Gold table/column has a comment.

## My notes

_(fill in as you go)_
