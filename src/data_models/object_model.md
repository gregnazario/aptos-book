# The Object Model

Objects similar to resource accounts, but rather than using a `SignerCapability` instead a `ExtendRef`
can be used to authenticate for the account. These have owners, and always have the resource `0x1::object::Object`
stored at its address.

TODO: Diagram


```mermaid
graph
  subgraph Account
    0x1::account::Account
  end
  subgraph Object
    subgraph 0x1::object::ObjectCore
      Owner
      
    end
    A[0x1::object::ObjectCore]
    B[0x42::example::Resource]
    C[0x1234::example2::Resource2]
  end
  
  Owner --> 0x1::account::Account
```