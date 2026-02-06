# Installation

The first step is to install the Aptos CLI. The CLI is a command-line interface(CLI) tool that allows you to interact
with the Aptos blockchain, including compiling, testing, and deploying Move modules, managing accounts, and reading and
writing data to the blockchain.

> Note: If you are using an unsupported platform or configuration, or you prefer to build a specific version from
> source, you can follow
> the [Building from Source](https://aptos.dev/en/build/cli/install-cli/install-cli-specific-version) guide on the Aptos
> developer docs.

The following instructions will tell you how to install the latest version of the Aptos CLI. It is highly recommended
to always use the latest version of the CLI, as it contains the latest features and bug fixes.

## Installing the Aptos CLI with Homebrew on macOS

For macOS, it's recommended to use Homebrew. To install the Aptos CLI on macOS, if you have Homebrew installed, you can
use the following command:

```bash
brew install aptos
```

## Installing the Aptos CLI on macOS and Linux

To install the Aptos CLI on macOS and Linux, you can use the following command:

```bash
curl -fsSL "https://aptos.dev/scripts/install_cli.sh" | sh
```

## Installing the Aptos CLI on Windows with Winget

For Windows users, you can use the Windows Package Manager (Winget) to install the Aptos CLI. Open a command prompt or
PowerShell and run the following command:

```powershell
winget install aptos.aptos-cli
```

## Installing the Aptos CLI on Windows

To install the Aptos CLI on Windows, you can use the following command in PowerShell:

```powershell
iwr "https://aptos.dev/scripts/install_cli.ps1" -useb | iex
```

## Troubleshooting

To check whether you have the Aptos CLI installed correctly, open a shell and enter this line:

```bash
aptos --version
```

You should see output similar to the following, with your CLI version.

```bash
aptos 7.6.0
```

If you see this information, you have installed the Aptos CLI successfully! If you don’t see this information, check
that the Aptos CLI is in your `%PATH%` system variable as follows.

In Windows CMD, use:

```console
echo %PATH%
```

In PowerShell, use:

```powershell
echo $env:Path
```

In Linux and macOS, use:

```shell
echo $PATH
```

## Updating the Aptos CLI

To update the Aptos CLI to the latest version, you can use the same command you used to install it. For example, if you
installed the CLI using Homebrew, you can run:

```bash
brew upgrade aptos
```

If you installed the CLI using the curl command, you can run the aptos update command:

```bash
aptos update aptos
```

Alternatively, you can run the installation command again:

```bash
curl -fsSL "https://aptos.dev/scripts/install_cli.sh" | sh
```

### Local Documentation

The Aptos CLI also provides local documentation that you can access by running the following command:

```bash
aptos --help
```

This command will display a list of available commands and options for the Aptos CLI, along with a brief description of
each command. You can also access the documentation for a specific command by running:

```bash
aptos <command> --help
```

### Text Editors and Integrated Development Environments

This book makes no assumptions about what tools you use to author Move code.
Just about any text editor will get the job done! However, many text editors and
integrated development environments (IDEs) have built-in support for Move:

- **VS Code**: Search for "Aptos Move Analyzer" in the VS Code Extensions Marketplace for syntax highlighting, go-to-definition, auto-completion, and error checking.
- **IntelliJ IDEA**: Search for "Move Language" in the JetBrains Plugin Marketplace for IDE support.
- **Vim/Neovim**: Community-maintained Move syntax highlighting plugins are available.
- **Emacs**: Community-maintained `move-mode` packages are available.

For the best development experience, VS Code with the Aptos Move Analyzer extension is recommended.

