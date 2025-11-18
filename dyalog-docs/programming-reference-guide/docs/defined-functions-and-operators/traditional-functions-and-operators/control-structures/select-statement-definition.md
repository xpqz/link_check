---
search:
  exclude: true
---

<h1 class="heading"><span class="name">:Select Statement</span></h1>

```
 
       |
       :Select aexp
       |
       |<----------------------------------------------.
       |                                               |
       .-------.-------.---------------.               |
       |       |       |               |               |
       |       :Else   :Case aexp      :CaseList aexp  |
       |       |       |               |               |
       |       |       |<--------------'               |
       |       |       |                               |
       |       code    code                            |
       |       |       |                               |
       |<------'       `-------------------------------'
       |
       :End[Select]
```
