import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:5173/');
  await page.getByRole('link', { name: 'Snapshot' }).click();
  await page.getByRole('button', { name: 'Today' }).click();
  const image = await page.waitForSelector('img');

  expect(image).not.toBeNull();
});
