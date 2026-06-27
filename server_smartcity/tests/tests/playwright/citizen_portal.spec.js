const path = require('path');
const { pathToFileURL } = require('url');
const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost:8000';
const SPA_PATH = path.resolve(__dirname, '..', '..', '..', 'smartcity_citizen_spa_24782077', 'index.html');
const SPA_URL = pathToFileURL(SPA_PATH).toString();

const TEST_CITIZEN_USERNAME = 'testwarga';
const TEST_CITIZEN_PASSWORD = 'testpassword123';
const TEST_ADMIN_USERNAME = 'admin';
const TEST_ADMIN_PASSWORD = 'admin123';

const EXPIRED_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjAwMDAwMDAwLCJpYXQiOjE2MDAwMDAwMDAsImp0aSI6ImZha2VfYWNjZXNzX2lkIiwidXNlcl9pZCI6MX0.fake_signature_for_testing';
const EXPIRED_REFRESH_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwMDAwMDAwMCwiaWF0IjoxNjAwMDAwMDAwLCJqdGkiOiJmYWtlX3JlZnJlc2hfaWQiLCJ1c2VyX2lkIjoxfQ.fake_signature_for_testing';
const VALID_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo5OTk5OTk5OTk5LCJpYXQiOjE2MDAwMDAwMDAsImp0aSI6InZhbGlkX2FjY2Vzc19pZCIsInVzZXJfaWQiOjF9.fake_valid_signature';

async function loginSPA(page, username, password) {
  await page.goto(`${SPA_URL}#login`);
  await page.waitForSelector('#loginForm', { state: 'visible', timeout: 10000 });
  await page.locator('#loginUsername').fill(username);
  await page.locator('#loginPassword').fill(password);
  await page.locator('#loginForm button[type="submit"]').click();
}

async function loginAdmin(page, username, password) {
  await page.goto(`${BASE_URL}/login/`);
  await page.waitForSelector('form', { state: 'visible', timeout: 10000 });
  await page.locator('input[name="username"]').fill(username);
  await page.locator('input[name="password"]').fill(password);
  await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle', timeout: 15000 }),
    page.locator('button[type="submit"]').click(),
  ]);
}

async function setupAuthTokens(page, accessToken, refreshToken, username = 'testwarga') {
  await page.evaluate(({ access, refresh, user }) => {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    localStorage.setItem('username', user);
  }, { access: accessToken, refresh: refreshToken, user: username });
}

async function clearAuthTokens(page) {
  await page.evaluate(() => {
    localStorage.clear();
  });
}

async function mockSPAApiUrl(page) {
  const base = 'http://localhost:8000';
  await page.route('**/api/**', async (route) => {
    const originalUrl = route.request().url();
    if (originalUrl.startsWith(base)) {
      return route.continue();
    }
    const urlObj = new URL(originalUrl);
    const newUrl = `${base}${urlObj.pathname}${urlObj.search}`;
    await route.continue({ url: newUrl });
  });
}

test.describe('Modul 1: Otorisasi & Sesi', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(SPA_URL);
    await clearAuthTokens(page);
    await mockSPAApiUrl(page);
  });

  test('AUTH-04: Akses #dashboard tanpa token → redirect ke #login', async ({ page }) => {
    const tokenBefore = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(tokenBefore).toBeNull();

    await page.goto(`${SPA_URL}#dashboard`);
    await page.waitForFunction(() => window.location.hash === '#login', null, { timeout: 5000 });
    await expect(page).toHaveURL(/#login/);

    const loginForm = page.locator('#loginForm');
    await expect(loginForm).toBeVisible({ timeout: 5000 });
  });

  test('AUTH-05: Token kadaluarsa → interceptor menangani 401 dan redirect ke #login', async ({ page }) => {
    await setupAuthTokens(page, EXPIRED_ACCESS_TOKEN, EXPIRED_REFRESH_TOKEN);
    await page.route('**/api/**', async (route) => {
      await route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Given token not valid for any token type', code: 'token_not_valid' }),
      });
    });

    page.on('dialog', async (dialog) => {
      await dialog.accept();
    });

    await page.goto(`${SPA_URL}#dashboard`);
    await page.waitForTimeout(2000);
    await page.waitForFunction(() => window.location.hash === '#login', null, { timeout: 10000 });
    await expect(page).toHaveURL(/#login/);

    const tokenAfter = await page.evaluate(() => localStorage.getItem('access_token'));
    const refreshAfter = await page.evaluate(() => localStorage.getItem('refresh_token'));
    expect(tokenAfter).toBeNull();
    expect(refreshAfter).toBeNull();
  });
});

test.describe('Modul 5: Interaktivitas UI', () => {
  test('UI-04: Klik tombol Buat Laporan → modal #reportModal muncul', async ({ page }) => {
    await page.goto(SPA_URL);
    await page.route('**/api/**', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ count: 0, results: [] }),
      });
    });
    await setupAuthTokens(page, VALID_ACCESS_TOKEN, EXPIRED_REFRESH_TOKEN);
    await page.goto(`${SPA_URL}#dashboard`);
    const btnBukaModal = page.locator('#btnBukaModal');
    await expect(btnBukaModal).toBeVisible({ timeout: 10000 });
    const reportModal = page.locator('#reportModal');
    await expect(reportModal).not.toBeVisible();
    await btnBukaModal.click();
    await expect(reportModal).toBeVisible({ timeout: 5000 });
  });
});
