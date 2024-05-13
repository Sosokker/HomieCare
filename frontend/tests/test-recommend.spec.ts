import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:5173/');

  const alertContainer = await page.waitForSelector('#alert-container');
  expect(alertContainer).not.toBeNull();
});
