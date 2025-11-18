---
search:
  exclude: true
---

<h1 class="heading"><span class="name">Booking Class</span></h1>

```apl
    :Class Booking
        :Field Public OK
        :Field Public Course
        :Field Public TeeTime
        :Field Public Message
        
        ∇ ctor args
          :Implements Constructor
          :Access Public Instance
          OK Course TeeTime Message←args
        ∇
        ∇ format
          :Implements Trigger OK,Message
          ⎕DF⍕Course TeeTime(⊃OK⌽Message'OK')
        ∇
    :EndClass
    
```
