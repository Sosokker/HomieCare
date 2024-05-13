import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:5173/');

  // Check if elements with specific text exist on the page
  const outdoorTempElement = await page
    .locator('span')
    .getByText(/^Outdoor Temperature$/)
    .first();
  const outdoorHumidityElement = await page
    .locator('span')
    .getByText(/^Outdoor Humidity$/)
    .first();
  const outdoorPM25Element = await page
    .locator('span')
    .getByText(/^Outdoor PM2.5$/)
    .first();
  const outdoorPM10Element = await page
    .locator('span')
    .getByText(/^Outdoor PM10$/)
    .first();
  const indoorTempElement = await page
    .locator('span')
    .getByText(/^Indoor Temperature$/)
    .first();
  const indoorLightElement = await page
    .locator('span')
    .getByText(/^Indoor Light$/)
    .first();

  expect(outdoorTempElement).not.toBeNull();
  expect(outdoorHumidityElement).not.toBeNull();
  expect(outdoorPM25Element).not.toBeNull();
  expect(outdoorPM10Element).not.toBeNull();
  expect(indoorTempElement).not.toBeNull();
  expect(indoorLightElement).not.toBeNull();
});
