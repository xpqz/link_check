---
search:
  exclude: true
---

<h1 class="heading"><span class="name">:If Statement</span></h1>

```
 
       |
       :If bexp
       |
       .-------.
       |       |
       |       andor
       |       |
       |<------'
       |
       code
       |
       |<------------------------------.
       |                               |
       .-------.-------.               |
       |       |       |               |
       |       :Else   :ElseIf bexp    |
       |       |       |               |
       |       |       .-------.       |
       |       |       |       |       |
       |       |       |       andor   |
       |       |       |       |       |
       |       |       |<------'       |
       |       |       |               |
       |       code    code            |
       |       |       |               |
       |<------'       `---------------'
       |
       :End[If]
       |
```
