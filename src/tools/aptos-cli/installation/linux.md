### Linux installation

Linux can be installed by a script.

Installing with curl:

```shell
curl -fsSL "https://aptos.dev/scripts/install_cli.sh" | sh
```

Installing with wget:

```shell
wget -qO- "https://aptos.dev/scripts/install_cli.sh" | sh
```

If you are getting `Illegal instruction` errors when running the CLI, it may be due to your CPU not supporting SIMD
instructions. Specifically for older non-SIMD processors or Ubuntu x86_64 docker containers on ARM Macs, you may need to
run the following command instead to skip SIMD instructions:

```bash
curl -fsSL "https://aptos.dev/scripts/install_cli.sh" | sh -s -- --generic-linux
```