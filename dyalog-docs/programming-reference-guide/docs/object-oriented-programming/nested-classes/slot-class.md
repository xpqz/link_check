---
search:
  exclude: true
---

<h1 class="heading"><span class="name">Slot Class</span></h1>

```apl

    :Class Slot
        :Field Public Time
        :Field Public Players
        
        ∇ ctor1 t
          :Implements Constructor
          :Access Public Instance
          Time←t
          Players←0⍴⊂''
        ∇
        ∇ ctor2 (t pl)
          :Implements Constructor
          :Access Public Instance
          Time Players←t pl
        ∇
        ∇ format
          :Implements Trigger Players
          ⎕DF⍕Time Players
        ∇
    :EndClass
```
