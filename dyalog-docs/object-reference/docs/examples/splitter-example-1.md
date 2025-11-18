---
search:
  exclude: true
---

<h1 class="heading"><span class="name">Splitter</span> <span class="right">Example 1</span></h1>


```apl
'F'⎕WC'Form' 'Vertical Splitter'('Size' 25 25)
'F.E1'⎕WC'Edit'(10 6⍴'Edit 1')('Style' 'Multi')
'F.E2'⎕WC'Edit'(10 6⍴'Edit 2')('Style' 'Multi')
'F.S'⎕WC'Splitter' 'F.E1' 'F.E2'
```


![](../img/split1.gif)


