package com.tsi.warehouse;

import com.tsi.util.CsvReader;

import java.io.FileInputStream;
import java.io.FileNotFoundException;

import java.io.FileReader;
import java.io.IOException;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

public final class Warehouse {

    private static final String DEFAULT_PRODUCTS_CSV_FILE = "products.csv";

    private final Map<Integer, Product> products;

    public Warehouse() throws FileNotFoundException, WarehouseException {
        this.products = new HashMap<>();
        readProducts();
    }

    private void readProducts() throws FileNotFoundException, WarehouseException {
        CsvReader reader = new CsvReader(new FileInputStream(DEFAULT_PRODUCTS_CSV_FILE));
        while (reader.hasNextRow()) {
            List<String> row = reader.nextRow();
            if (row.isEmpty()) {
                continue;
            }
            int id;
            try {
                id = Integer.valueOf(row.get(0));
            } catch (NumberFormatException ex) {
                throw new WarehouseException("Failed to read products: invalid product ID in CSV, must be an integer.", ex);
            }
            String name = row.get(1);
            double price;
            try {
                price = Double.valueOf(row.get(2));
            } catch (NumberFormatException ex) {
                throw new WarehouseException("Failed to read products: invalid price in CSV, must be an integer.", ex);
            }
            if (products.containsKey(id)) {
                throw new WarehouseException("Failed to read products: duplicate product ID in CSV.");
            }
            products.put(id, new Product(id, name, price));
        }
    }

    public Collection<Product> getProducts() {
        return products.values();
    }
}
