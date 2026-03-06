import { describe, expect, it } from "vitest";

import config, { buildPlaywrightConfig } from "../../playwright.config";

/**
 * Keep the Phase 00 executable web baseline under test so the repository does
 * not carry unverified configuration code into Phase 01.
 */
describe("playwright config baseline", () => {
  it("uses the expected e2e test directory and reporters", () => {
    expect(config.testDir).toBe("./tests/e2e");
    expect(config.reporter).toEqual([
      ["list"],
      [
        "html",
        {
          open: "never",
          outputFolder: "../../output/playwright/report",
        },
      ],
    ]);
    expect(config.fullyParallel).toBe(true);
    expect(config.forbidOnly).toBe(Boolean(process.env.CI));
  });

  it("captures the expected artifact behavior on failure and retry", () => {
    expect(config.retries).toBe(process.env.CI ? 2 : 0);

    expect(config.use).toMatchObject({
      screenshot: "only-on-failure",
      trace: "on-first-retry",
      video: "retain-on-failure",
    });
  });

  it("defines the cross-browser baseline projects", () => {
    expect(config.projects).toHaveLength(3);
    expect((config.projects ?? []).map((project) => project.name)).toEqual([
      "chromium",
      "firefox",
      "webkit",
    ]);
  });

  it("covers both local and CI config branches explicitly", () => {
    const localConfig = buildPlaywrightConfig({
      baseURL: "http://127.0.0.1:4000",
      ci: false,
    });
    const ciConfig = buildPlaywrightConfig({
      baseURL: "http://127.0.0.1:5000",
      ci: true,
    });

    expect(localConfig.retries).toBe(0);
    expect(localConfig.workers).toBeUndefined();
    expect(localConfig.use?.baseURL).toBe("http://127.0.0.1:4000");

    expect(ciConfig.retries).toBe(2);
    expect(ciConfig.workers).toBe(2);
    expect(ciConfig.use?.baseURL).toBe("http://127.0.0.1:5000");
  });
});
