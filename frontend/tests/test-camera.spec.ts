import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:5173/');
  await page.getByRole('link', { name: 'Camera' }).click();
  await page.getByRole('combobox').selectOption('2');
  await page.getByRole('button', { name: 'Start Connection' }).click();
  await page.waitForSelector('text=Loading...');
  const loadingText = await page.$('text=Loading...');
  expect(loadingText).not.toBeNull();

  // await page.waitForSelector('text=Loading...', { state: 'hidden' });
  // const hiddenLoadingText = await page.$('text=Loading...');
  // expect(hiddenLoadingText).toBeNull();

  await page.waitForSelector('canvas');
  const canvas = await page.$('canvas');
  expect(canvas).not.toBeNull();
});
