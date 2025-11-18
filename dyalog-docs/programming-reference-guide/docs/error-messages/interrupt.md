




<h1 class="heading"><span class="name">INTERRUPT</span> <span class="command">1003</span></h1>



This report is given when execution is suspended by entering a hard interrupt.  A hard interrupt causes execution to suspend as soon as possible without leaving the environment in a damaged state.

<h2 class="example">Example</h2>
```apl
      1 1 2 ⍉(2 100⍴⍳200)∘.|?1000⍴200
```


(Hard interrupt)
```apl
INTERRUPT
      1 1 2 ⍉(2 100⍴⍳200)∘.|?1000⍴200
            ^
```



