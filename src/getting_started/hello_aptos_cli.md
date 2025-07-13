# Hello Aptos CLI!

## Introduction

The Aptos CLI is a powerful command-line interface that allows you to interact with the Aptos blockchain. It provides a
wide range of commands to manage accounts, deploy smart contracts, and perform various operations on the blockchain.

You will become familiar with it the longer you develop on the Aptos blockchain, as it is a key tool for compiling,
testing, deploying, and interacting with contracts on the Aptos blockchain.

## Installation

If you haven't already installed the Aptos CLI, please refer to the [Installation guide](installation.md) for
instructions on how to install it on your system. The CLI is available for macOS, Linux, and Windows for both x86 and
ARM systems.

## Hello Aptos CLI

In this section, we will explore some basic commands of the Aptos CLI to interact with the blockchain. We will cover
submitting transactions and querying accounts.

### Initializing the CLI

First, determine whether you want a `workspace` style config or a `global` style config. By default, it uses `workspace`
which means credentials and configuration will be based in your current directory. When you change directories, you will
not use those credentials, and then will need to create different ones for each directory. If you want a `global` config
that is shared among all directories, run the following command:

```sh
aptos config set-global-config --config-type global
```

Once we've set that, we will need to create the `default` profile for the Aptos CLI. This profile will store your
account keys and create an account for you to use with the CLI. To initialize the CLI, run the following command in your
terminal:

```sh
aptos init
```

This command will prompt you to create a new account if you have not already created one. It will look something like
this:

```sh
$ aptos init
Configuring for profile default
Choose network from [devnet, testnet, mainnet, local, custom | defaults to devnet]
```

You can choose the network you want to connect to. For this example, we will use the `devnet` network, which is a short
lived test network that is reset once a week. It is a great place to start experimenting with the Aptos CLI and easy to
ignore your early mistakes. You can just press `Enter` to select the default `devnet` network.

Next, it will prompt you to enter your private key. If you do not have a private key, you can generate a new one by just
pressing `Enter`. If you have a private key, you can enter it as a hex literal (starting with `0x`). The prompt will
look like this:

```sh
Enter your private key as a hex literal (0x...) [Current: Redacted | No input: Generate new key (or keep one if present)]
```

The CLI will then automatically fund and create an account for you on the `devnet` network. You will see output similar
to the following:

```sh
Account 0x78077fe8db589e1a3407170cf8af3bd60a8c95737918c15dd6f49dcbecc7900a is not funded, funding it with 100000000 Octas
Account 0x78077fe8db589e1a3407170cf8af3bd60a8c95737918c15dd6f49dcbecc7900a funded successfully

---
Aptos CLI is now set up for account 0x78077fe8db589e1a3407170cf8af3bd60a8c95737918c15dd6f49dcbecc7900a as profile default!
---

{
  "Result": "Success"
}
```

This means that your account is now set up and ready to use with the Aptos CLI!

Similarly, you can create additional profiles by running the `aptos init` command with the `--profile <profile_name>`.
Then any of those accounts can be used with the CLI by specifying the `--profile <profile_name>` flag in your commands.

Additionally, if you want to change the network for your profile, you can use the `aptos init` command again to change
the network:

```sh
aptos init --profile default --network <network_name>
```

## Submitting a Transaction

Now that we have initialized the CLI and created an account, we can submit a transaction to the blockchain. For this
example, we will send some Octas (subunit of the native APT token of the Aptos blockchain) from our account to another
account.

To send Octas, we will use the `aptos account transfer` command. This command allows you to send funds to an account
on the blockchain. The command syntax is as follows:

```sh
aptos account transfer --account <recipient_address> --amount <amount>
```

Note that the `--account` flag is used to specify the recipient's address, and the `--amount` flag is used to specify
the amount to send in Octas. For example, to send 10 Octas to the account
`0x78077fe8db589e1a3407170cf8af3bd60a8c95737918c15dd6f49dcbecc7900a`, you would run:

```sh
aptos account transfer --account 0x78077fe8db589e1a3407170cf8af3bd60a8c95737918c15dd6f49dcbecc7900a --amount 10
```