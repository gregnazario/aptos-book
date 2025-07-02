### Windows installation

Only Windows 10 or newer is supported. If you use an existing package manager `choco`, `scoop`, or `winget` you can
simply run the appropriate command:

```powershell
choco install aptos
```

```powershell
scoop install https://aptos.dev/scoop/aptos.json
```

```powershell
winget install aptos
```

If a package manager does not work for you, a `PowerShell` script is provided. Please open a Windows PowerShell window and
run:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser;
iwr https://aptos.dev/scripts/install_cli.ps1 | iex
```