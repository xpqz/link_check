---
search:
  exclude: true
---

<h1 class="heading"><span class="name">GolfCourse Class</span></h1>

```apl

    :Class GolfCourse
        :Field Public Code←¯1
        :Field Public Name←''
        
        ∇ ctor args
          :Implements Constructor
          :Access Public Instance
          Code Name←args
          ⎕DF Name,'(',(⍕Code),')'
        ∇
    
    :EndClass
    
```
