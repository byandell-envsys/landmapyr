# Dependabot

**`dependabot[bot]` is not a malicious bot.** It is a legitimate, built-in security tool provided by GitHub to help keep your project dependencies secure.

### Why did you see this?

GitHub automatically runs Dependabot on repositories to check for out-of-date or vulnerable packages (listed in your `pyproject.toml`). When it detects one, it automatically opens a pull request (PR) to update the package. When these PRs are opened, they trigger your standard GitHub Actions workflow (`CI` or GitHub Pages build) on the PR branch, which shows up in your Action runs under the actor `dependabot[bot]`.

---

### What should you do?

#### Option A: Keep it (Recommended)

If you want to keep your dependencies secure, you don't need to do anything. Dependabot will keep submitting PRs for vulnerable libraries. You can review and merge them as you like to keep your packages updated.

#### Option B: Turn it off via GitHub Settings

If you find it noisy or do not want it running checks on your repository, you can disable it directly in your GitHub settings:

1. Go to your repository page on GitHub.
2. Click on **Settings** (the gear icon at the top).
3. In the left sidebar, click on **Code security and analysis**.
4. Scroll down to **Dependabot security updates** and click **Disable**.
5. Do the same for **Dependabot version updates** (if enabled).

#### Option C: Limit it via configuration file

If you want to control what Dependabot updates (e.g., only run it monthly or ignore certain packages), you can create a file at `.github/dependabot.yml` in your repository. For example:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "monthly" # Run monthly instead of daily/on-every-change
```
