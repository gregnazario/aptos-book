# CLI Installation Methods

[![Packaging status](https://repology.org/badge/vertical-allrepos/aptos.svg)](https://repology.org/project/aptos/versions)

## macOS

### Homebrew

#### Installation

To install the Aptos CLI on macOS, you can use Homebrew, a popular package manager. Open your terminal and run the
following command:

```bash
brew install aptos
```

#### Upgrading

To upgrade the Aptos CLI using Homebrew, run:

```bash
brew upgrade aptos
```

### Script Installation

#### Installation

To install the Aptos CLI using a script, you can use the following command in your terminal:

```bash
curl -sSfL https://aptos.dev/scripts/install_cli.sh | sh
```

#### Upgrading

To upgrade the Aptos CLI using the script, you can run the same command again:

```bash
curl -sSfL https://aptos.dev/scripts/install_cli.sh | sh
```

## Linux

### Script Installation

#### Installation

To install the Aptos CLI on Linux, you can use the following command in your terminal:

```bash
curl -sSfL https://aptos.dev/scripts/install_cli.sh | sh
```

#### Upgrading

To upgrade the Aptos CLI using the script, you can use the CLI:

```bash
aptos update aptos
```

Or you can run the installation command again:

```bash
curl -sSfL https://aptos.dev/scripts/install_cli.sh | sh
```

> If you are getting `Illegal instruction` errors when running the CLI, it may be due to your CPU not supporting SIMD
> instructions. Specifically for older non-SIMD processors or Ubuntu x86_64 docker containers on ARM Macs, you may need to
> run the following command instead to skip SIMD instructions:

```bash
curl -fsSL "https://aptos.dev/scripts/install_cli.sh" | sh -s -- --generic-linux
```

## Windows

### Winget

#### Installation

To install the Aptos CLI on Windows using Winget, open a command prompt or PowerShell and run the following command:

```powershell
winget install aptos.aptos-cli
```

#### Upgrading

To upgrade the Aptos CLI using Winget, run:

```powershell
winget upgrade aptos.aptos-cli
```

### Chocolatey

#### Installation

To install the Aptos CLI on Windows using Chocolatey, open a command prompt or PowerShell with administrative privileges
and run:

```powershell
choco install aptos-cli
```

#### Upgrading

To upgrade the Aptos CLI using Chocolatey, run:

```powershell
choco upgrade aptos-cli
```

### Script Installation

#### Installation

To install the Aptos CLI on Windows using a script, you can use the following command in PowerShell:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser;
iwr https://aptos.dev/scripts/install_cli.ps1 | iex
```

#### Upgrading

To upgrade the Aptos CLI using the script, you can use the CLI:

```powershell
aptos update aptos
```

Or you can run the installation command again:

```powershell
Invoke-WebRequest -Uri "https://aptos.dev/scripts/install_cli.ps1" -OutFile "install_cli.ps1"; .\install_cli.ps1
```

