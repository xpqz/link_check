---
search:
  exclude: true
---

<h1 class="heading"><span class="name">StartingSheet Class</span></h1>

```apl

    :Class StartingSheet
        :Field Public OK
        :Field Public Course
        :Field Public Date
        :Field Public Slots←⎕NULL
        :Field Public Message
        
        ∇ ctor args
          :Implements Constructor
          :Access Public Instance
          OK Course Date←args
        ∇
        ∇ format
          :Implements Trigger OK,Message
          ⎕DF⍕2 1⍴(⍕Course Date)(↑⍕¨Slots)
        ∇
    :EndClass
    
```
