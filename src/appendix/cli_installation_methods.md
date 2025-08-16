# CLI Installation Methods

This appendix provides detailed instructions for installing and upgrading the Aptos CLI on various operating systems. For a quick start, see the [Installation](getting_started/installation.md) page.

[![Packaging status](https://repology.org/badge/vertical-allrepos/aptos.svg)](https://repology.org/project/aptos/versions)

---

## macOS

### Homebrew (Recommended)

**To install:**

```bash
brew install aptos
```

**To upgrade:**

```bash
brew upgrade aptos
```

### Script Installation

Run the following command for both initial installation and upgrading:

```bash
curl -sSfL https://aptos.dev/scripts/install_cli.sh | sh
```

---

## Linux

### Script Installation

**To install:**

```bash
curl -sSfL https://aptos.dev/scripts/install_cli.sh | sh
```

> **Note on CPU Compatibility**
> If you encounter an `Illegal instruction` error, your CPU may not support certain SIMD instructions. This can happen on older processors or when running in specific virtualized environments (e.g., Ubuntu x86_64 on an ARM Mac).
>
> Use the following command instead for a generic build:
>
> ```bash
> curl -fsSL "https://aptos.dev/scripts/install_cli.sh" | sh -s -- --generic-linux
> ```

**To upgrade:**

You can either use the built-in update command:

```bash
aptos update aptos
```

Or, re-run the installation script:

```bash
curl -sSfL https://aptos.dev/scripts/install_cli.sh | sh
```

---

## Windows

### Winget (Recommended)

**To install:**

```powershell
winget install aptos.aptos-cli
```

**To upgrade:**

```powershell
winget upgrade aptos.aptos-cli
```

### Chocolatey

**To install** (in an administrative shell):

```powershell
choco install aptos-cli
```

**To upgrade** (in an administrative shell):

```powershell
choco upgrade aptos-cli
```

### Script Installation

**To install:**

Run the following command in PowerShell. This will set the execution policy for the current user and then run the installer.

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser; iwr https://aptos.dev/scripts/install_cli.ps1 | iex
```

**To upgrade:**

You can either use the built-in update command:

```powershell
aptos update aptos
```

Or, re-run the installation script:

```powershell
iwr https://aptos.dev/scripts/install_cli.ps1 | iex
```
