---
search:
  exclude: true
---

<h1 class="heading"><span class="name">:While Statement</span></h1>

```
 
       |
       :While bexp
       |
       .-------.
       |       |
       |       andor
       |       |
       |<------'
       |
       code
       |
       .---------------.
       |               |
       :End[While]     :Until bexp
       |               |
       |               .-------.
       |               |       |
       |               |       andor
       |               |       |
       |               |<------'
       |               |
       |<--------------'
       |
```
