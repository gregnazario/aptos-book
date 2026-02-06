# Building AI Agents on Aptos

AI agents are autonomous programs that can interact with the blockchain on behalf of users. Aptos provides infrastructure for building AI agents that can manage digital assets, execute DeFi strategies, and participate in governance.

## What is an On-Chain AI Agent?

An on-chain AI agent typically consists of:

1. **An off-chain LLM** that makes decisions based on on-chain data
2. **A wallet/account** that the agent controls for executing transactions
3. **Smart contracts** that define what the agent can do and enforce guardrails
4. **An execution loop** that reads state, decides on actions, and submits transactions

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│                  │     │                  │     │                 │
│   LLM Engine    │────▶│  Agent Backend   │────▶│  Aptos Chain    │
│  (Decision)     │     │  (Execution)     │     │  (Settlement)   │
│                  │◀────│                  │◀────│                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## Agent Architecture

### 1. Read On-Chain State

Use the Aptos SDK to read blockchain state:

```typescript
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

const aptos = new Aptos(new AptosConfig({ network: Network.MAINNET }));

// Read account balance
const balance = await aptos.getAccountAPTAmount({
  accountAddress: agentAddress,
});

// Read contract state via view function
const state = await aptos.view({
  payload: {
    function: "0x1::coin::balance",
    typeArguments: ["0x1::aptos_coin::AptosCoin"],
    functionArguments: [agentAddress],
  },
});
```

### 2. LLM Decision Making

Feed the on-chain state to an LLM for decision-making:

```typescript
const prompt = `
You are an AI agent managing a DeFi portfolio on Aptos.

Current state:
- APT balance: ${balance}
- Current positions: ${JSON.stringify(positions)}
- Market conditions: ${JSON.stringify(marketData)}

Available actions:
1. swap(token_in, token_out, amount) - Swap tokens on a DEX
2. provide_liquidity(pool, amount) - Add liquidity to a pool
3. stake(amount) - Stake APT with a validator
4. hold() - Take no action

Decide the best action based on the current state.
Return your decision as JSON: { "action": "...", "params": {...}, "reasoning": "..." }
`;

const decision = await llm.complete(prompt);
```

### 3. Execute Transactions

Submit the decided transaction to the blockchain:

```typescript
import { Account, Ed25519PrivateKey } from "@aptos-labs/ts-sdk";

// Agent's account (secured in practice)
const agentAccount = Account.fromPrivateKey({
  privateKey: new Ed25519PrivateKey(agentPrivateKey),
});

// Build and submit the transaction
const transaction = await aptos.transaction.build.simple({
  sender: agentAccount.accountAddress,
  data: {
    function: "0x1::coin::transfer",
    typeArguments: ["0x1::aptos_coin::AptosCoin"],
    functionArguments: [recipientAddress, amount],
  },
});

const committedTxn = await aptos.signAndSubmitTransaction({
  signer: agentAccount,
  transaction,
});

await aptos.waitForTransaction({
  transactionHash: committedTxn.hash,
});
```

## Smart Contract Guardrails

For safety, define on-chain guardrails that limit what an agent can do:

```move
module my_addr::agent_vault {
    use std::signer;

    /// Maximum amount the agent can transfer in a single transaction
    const MAX_TRANSFER: u64 = 1000000; // 0.01 APT

    /// Maximum daily spend
    const MAX_DAILY_SPEND: u64 = 100000000; // 1 APT

    struct AgentConfig has key {
        owner: address,
        daily_spent: u64,
        last_reset_timestamp: u64,
        max_transfer: u64,
        max_daily_spend: u64,
        is_active: bool,
    }

    /// Only the agent owner can configure the agent
    public entry fun configure_agent(
        owner: &signer,
        max_transfer: u64,
        max_daily_spend: u64,
    ) {
        let owner_addr = signer::address_of(owner);
        // Store configuration...
    }

    /// The agent calls this -- guardrails enforce limits
    public entry fun agent_transfer(
        agent: &signer,
        to: address,
        amount: u64,
    ) acquires AgentConfig {
        let agent_addr = signer::address_of(agent);
        let config = &mut AgentConfig[agent_addr];

        assert!(config.is_active, 1); // Agent must be active
        assert!(amount <= config.max_transfer, 2); // Per-transaction limit
        assert!(config.daily_spent + amount <= config.max_daily_spend, 3); // Daily limit

        config.daily_spent = config.daily_spent + amount;
        // Execute transfer...
    }

    /// Owner can pause the agent at any time
    public entry fun pause_agent(owner: &signer) acquires AgentConfig {
        let config = &mut AgentConfig[signer::address_of(owner)];
        config.is_active = false;
    }
}
```

## Agent Frameworks on Aptos

Several frameworks simplify building AI agents on Aptos:

### Move Agent Kit

The Move Agent Kit provides tools for building AI agents that interact with the Aptos blockchain. It integrates with popular LLM frameworks and provides pre-built tools for common on-chain actions.

### Key features:
- Pre-built Aptos transaction tools for LLM agents
- Integration with LangChain, Eliza, and other agent frameworks
- Token transfer, NFT minting, and DeFi interaction tools
- Wallet management and transaction signing

### Eliza Framework

The Eliza Framework is a multi-agent simulation framework that supports Aptos blockchain interactions. Agents can:
- Manage Aptos wallets
- Execute token transfers
- Interact with DeFi protocols
- Monitor on-chain events

## Use Cases

### Portfolio Manager

An AI agent that:
- Monitors token prices and portfolio performance
- Rebalances holdings based on predefined strategies
- Executes swaps on DEXes for optimal pricing
- Reports performance to the owner

### NFT Trader

An AI agent that:
- Monitors NFT marketplace listings
- Evaluates NFT value using image analysis and market data
- Places bids or buys undervalued NFTs
- Lists overvalued NFTs for sale

### Governance Participant

An AI agent that:
- Reads governance proposals
- Analyzes proposal impact using LLM reasoning
- Votes according to predefined principles
- Reports voting activity and reasoning

## Security Considerations

1. **Key management**: Agent private keys must be securely stored (use HSMs or secure enclaves).
2. **Spending limits**: Always enforce on-chain guardrails for maximum transaction amounts.
3. **Kill switch**: Implement an owner-controlled pause mechanism.
4. **Monitoring**: Log all agent actions and set up alerts for unusual behavior.
5. **Testing**: Thoroughly test agent behavior on devnet before mainnet deployment.
6. **Prompt injection**: Protect against prompt injection attacks if the agent processes external data.

## Best Practices

1. **Start small**: Begin with simple, low-risk actions and gradually increase agent capabilities.
2. **Use guardrails**: Always implement on-chain spending limits and pause mechanisms.
3. **Monitor continuously**: Watch agent behavior and be ready to intervene.
4. **Test extensively**: Run agents on devnet with simulated market conditions.
5. **Separate concerns**: Keep the LLM decision-making separate from transaction execution.
6. **Audit agent contracts**: The smart contracts that enforce guardrails are security-critical.
