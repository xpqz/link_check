---
search:
  exclude: true
---

<h1 class="heading"><span class="name">:Trap Statement</span></h1>

```
 
       |
       :Trap <ecode>
       |
       code
       |
       |<------------------------------------.
       |                                     |
       .-------.-------.                     |
       |       |       |                     |
       |       :Else   :Case[List] <ecode>   |
       |       |       |                     |
       |       |       |                     |
       |       |       |                     |
       |       code    code                  |
       |       |       |                     |
       |<------'       `---------------------'
       |
       :End[Trap]
       |
```

Where `ecode` is a scalar or vector of `⎕TRAP` event codes.

Note that within the `:Trap` control structure, `:Case` is used for a single event code and `:CaseList` for a vector of event codes.
