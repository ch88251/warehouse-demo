package com.tsi.warehouse;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertNotNull;

public class WarehouseTest {


    @Test
    void testWarehouseInitialization() {
        assertDoesNotThrow(() -> {
            Warehouse warehouse = new Warehouse();
            assertNotNull(warehouse);
        });
    }
}
