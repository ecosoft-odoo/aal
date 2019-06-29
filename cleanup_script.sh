#!/bin/bash
pg_container="postgres-11.2"
pg_user="odoo"
db="AAL"
psql="docker exec -it $pg_container psql -U $pg_user $db"

# Inventory
$psql -c "delete from stock_picking_product_kit_helper"
$psql -c "delete from stock_move_line"
$psql -c "delete from stock_move"
$psql -c "delete from stock_picking"
$psql -c "delete from stock_inventory_line"
$psql -c "delete from stock_inventory"
$psql -c "delete from stock_quant"

# Sales
$psql -c "delete from sale_order_option"
$psql -c "delete from sale_order_line"
$psql -c "delete from sale_order"

# Purchase
$psql -c "delete from purchase_order_line"
$psql -c "delete from purchase_order"

# Manufactoring
$psql -c "delete from mrp_bom_line"
$psql -c "delete from mrp_bom"
$psql -c "delete from mrp_production"

# Invoicing
$psql -c "delete from account_partial_reconcile";
$psql -c "delete from account_move_line"
$psql -c "delete from account_invoice_tax"
$psql -c "delete from account_invoice_line"
$psql -c "delete from account_invoice"
$psql -c "delete from account_move"
$psql -c "delete from account_billing"
$psql -c "delete from account_payment"

# Product
$psql -c "delete from product_supplierinfo"
