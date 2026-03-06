/**
 * Build the Phase 00 Playwright baseline deterministically so both local and CI
 * branches can be exercised under test.
 */
import { defineConfig, devices } from "@playwright/test";

type PlaywrightConfigOptions = {
  baseURL?: string;
  ci?: boolean;
};

/**
 * Return the canonical Playwright baseline for this repository.
 */
export function buildPlaywrightConfig(
  options: PlaywrightConfigOptions = {},
) {
  const isCI = options.ci ?? Boolean(process.env.CI);
  const baseURL =
    options.baseURL ?? process.env.PLAYWRIGHT_BASE_URL ?? "http://127.0.0.1:3000";

  return defineConfig({
    testDir: "./tests/e2e",
    testMatch: "**/*.e2e.spec.ts",
    fullyParallel: true,
    forbidOnly: isCI,
    retries: isCI ? 2 : 0,
    ...(isCI ? { workers: 2 } : {}),
    reporter: [
      ["list"],
      [
        "html",
        {
          open: "never",
          outputFolder: "../../output/playwright/report",
        },
      ],
    ],
    outputDir: "../../output/playwright/test-results",
    use: {
      baseURL,
      trace: "on-first-retry",
      screenshot: "only-on-failure",
      video: "retain-on-failure",
    },
    projects: [
      {
        name: "chromium",
        use: {
          ...devices["Desktop Chrome"],
        },
      },
      {
        name: "firefox",
        use: {
          ...devices["Desktop Firefox"],
        },
      },
      {
        name: "webkit",
        use: {
          ...devices["Desktop Safari"],
        },
      },
    ],
  });
}

export default buildPlaywrightConfig();
