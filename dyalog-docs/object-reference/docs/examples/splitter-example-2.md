---
search:
  exclude: true
---

<h1 class="heading"><span class="name">Splitter</span> <span class="right">Example 2</span></h1>


```apl
'F'⎕WC'Form' 'Horizontal Splitter'('Size' 25 25)
'F.E1'⎕WC'Edit'(5 6⍴'Edit 1')('Style' 'Multi')
'F.E2'⎕WC'Edit'(5 6⍴'Edit 2')('Style' 'Multi')
'F.S'⎕WC'Splitter' 'F.E1' 'F.E2'('Style' 'Horz')
```


![](../img/split2.gif)


