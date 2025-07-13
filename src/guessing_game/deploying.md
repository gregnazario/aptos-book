# Deploying the Contract

To deploy the contract, we'll use the Aptos CLI. We'll assume you have already run the command `aptos init` for the
default profile. If you have not, go check out the [hello_aptos_cli tutorial](../getting_started/hello_aptos_cli.md).

In order to deploy the contract, we'll run the below command that will compile the contract, and then ask you if you're
sure that you want to deploy it.

```sh
aptos move deploy --named-addresses module_addr=default
```

Once it's deployed, you should be able to see your contract on your network and your address in
the [Aptos Explorer](https://explorer.aptoslabs.com). This uploads your source code by default, so it's easily
verifiable and easy to tell which functions are which.

## Upgrading the Contract

To upgrade the contract, simply run the command again:

```sh
aptos move deploy --named-addresses module_addr=default
```