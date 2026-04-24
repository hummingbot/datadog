const { test, expect } = require('@playwright/test');

test.describe('Hummingbot Volume Dashboard', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('http://localhost:8080');
        // Wait for data to load
        await page.waitForSelector('#total-volume:not(:has-text("-"))');
    });

    test('should load and display data', async ({ page }) => {
        // Check title
        await expect(page.locator('h1')).toContainText('Hummingbot Reported Volumes');

        // Check stats are populated
        const totalVolume = await page.locator('#total-volume').textContent();
        expect(totalVolume).toMatch(/\$[\d.]+[BMK]?/);

        const totalExchanges = await page.locator('#total-exchanges').textContent();
        expect(parseInt(totalExchanges)).toBeGreaterThan(0);

        // Check charts rendered (use first() since ApexCharts creates multiple SVGs)
        await expect(page.locator('#daily-volume-chart svg').first()).toBeVisible();
        await expect(page.locator('#exchange-chart svg').first()).toBeVisible();

        // Check table has data
        const rows = await page.locator('#exchange-table tbody tr').count();
        expect(rows).toBeGreaterThan(5);
    });

    test('should filter by time range', async ({ page }) => {
        // Get initial total volume
        const initialVolume = await page.locator('#total-volume').textContent();

        // Select Last 30 Days
        await page.selectOption('#time-range', '30');
        await page.waitForTimeout(500);

        // Volume should change (likely be less)
        const filteredVolume = await page.locator('#total-volume').textContent();
        expect(filteredVolume).not.toBe(initialVolume);

        // Date range text should update (format: YYYY-MM-DD → YYYY-MM-DD)
        const dateRange = await page.locator('#date-range').textContent();
        expect(dateRange).toMatch(/\d{4}-\d{2}-\d{2}/);
    });

    test('should filter by exchange using multi-select', async ({ page }) => {
        // Get initial exchange count
        const initialCount = await page.locator('#total-exchanges').textContent();
        expect(parseInt(initialCount)).toBeGreaterThan(10);

        // Open exchange dropdown
        await page.click('#exchange-button');
        await expect(page.locator('#exchange-dropdown')).toBeVisible();

        // Search for binance
        await page.fill('#exchange-search', 'binance');
        await page.waitForTimeout(300);

        // Clear all first
        await page.click('.btn-clear-all');
        await page.waitForTimeout(300);

        // Check that count updated to 0
        const zeroCount = await page.locator('#total-exchanges').textContent();
        expect(parseInt(zeroCount)).toBe(0);

        // Select just binance
        const binanceCheckbox = page.locator('.multi-select-option').filter({ hasText: 'binance' }).first().locator('input');
        await binanceCheckbox.check();
        await page.waitForTimeout(300);

        // Should now show 1 exchange
        const oneCount = await page.locator('#total-exchanges').textContent();
        expect(parseInt(oneCount)).toBe(1);

        // Table should only show binance
        const tableText = await page.locator('#exchange-table tbody').textContent();
        expect(tableText.toLowerCase()).toContain('binance');
    });

    test('should have working Select All / Clear All buttons', async ({ page }) => {
        // Open dropdown
        await page.click('#exchange-button');

        // Clear all
        await page.click('.btn-clear-all');
        await page.waitForTimeout(300);

        const clearedCount = await page.locator('#total-exchanges').textContent();
        expect(parseInt(clearedCount)).toBe(0);

        // Select all
        await page.click('.btn-select-all');
        await page.waitForTimeout(300);

        const allCount = await page.locator('#total-exchanges').textContent();
        expect(parseInt(allCount)).toBeGreaterThan(50);
    });

    test('should show custom date range inputs', async ({ page }) => {
        // Initially hidden
        await expect(page.locator('#start-date-group')).toBeHidden();
        await expect(page.locator('#end-date-group')).toBeHidden();

        // Select custom
        await page.selectOption('#time-range', 'custom');

        // Now visible
        await expect(page.locator('#start-date-group')).toBeVisible();
        await expect(page.locator('#end-date-group')).toBeVisible();
    });

    test('should update charts when filters change', async ({ page }) => {
        // Take screenshot of initial state
        const initialChart = await page.locator('#exchange-chart').screenshot();

        // Filter to last 30 days
        await page.selectOption('#time-range', '30');
        await page.waitForTimeout(500);

        // Chart should have changed
        const filteredChart = await page.locator('#exchange-chart').screenshot();
        expect(Buffer.compare(initialChart, filteredChart)).not.toBe(0);
    });
});
