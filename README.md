# Agent Nextus downloads

Desktop builds of **Agent Nextus**, by [AretEpoch AI](https://aretepochai.com).
The official product website is [agentnextus.com](https://agentnextus.com/).

This repository distributes release binaries and checksums. It does not contain
the private application repository, development history, user rooms or credentials.

## Preview builds

Windows installer, Linux AppImage/DEB and macOS Apple Silicon/Intel packages are
published only after native startup verification. See each release for its
available files. Do not use GitHub's automatically generated source-code archives
as an application download: those archives contain this download page only.

The app includes its own interface, Node runtime, SQLite dependencies, Git,
Codex and Gemini CLI. Providers offers an explicit Claude Code installation from
Anthropic's official npm package; it is downloaded to the user's own data folder.
Provider sign-in, eligibility, usage limits and charges remain separate.
Other providers/local inference applications may need their own installations.

These initial previews are not signed/notarized. Code-signing certificates have
not been configured. macOS Gatekeeper and Windows SmartScreen may flag an unknown
publisher; the app does not disable those protections. Use a signed release if
your device policy requires one. Linux needs its normal desktop libraries and a
working Chromium sandbox; DEB declares system dependencies. Saving optional API
keys/MCP secrets on Linux requires an OS keyring and `secret-tool`.

Rooms, workspaces, attachments and managed tools live in the per-user application
data folder, separately from installation files. A newer desktop installer retains
that data. The development checkout uses a different database and is not imported
automatically. Quit the older source launcher before opening the desktop download;
both use local port 3001.

Release checksums use SHA-256. Verify a downloaded file against SHA256SUMS.txt.
Third-party licenses and source references are supplied under
`resources/nextus/THIRD-PARTY-NOTICES.txt` and `THIRD-PARTY-SOURCES.txt` (inside the
app bundle's Resources directory on macOS). Original third-party license files
remain next to their components. Agent Nextus application code is proprietary;
third-party components retain their own licenses and copyrights.
