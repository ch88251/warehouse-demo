package com.tsi.warehouse;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class WarehouseTest {


    @Test
    void testWarehouseInitialization() {
        assertDoesNotThrow(() -> {
            Warehouse warehouse = new Warehouse();
            assertNotNull(warehouse);
            assertNotNull(warehouse.getProducts());
            assertFalse(warehouse.getProducts().isEmpty());
        });
    }
}
