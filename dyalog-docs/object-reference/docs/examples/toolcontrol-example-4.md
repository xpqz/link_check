---
search:
  exclude: true
---

<h1 class="heading"><span class="name">ToolControl</span> <span class="right">Example 4</span></h1>


```apl
'F'⎕WC'Form' 'ToolControl with MenuBar'('Size' 20 40)
'F.TB'⎕WC'ToolControl'

:With 'F.TB.MB'⎕WC'MenuBar'
    :With 'File'⎕WC'Menu' 'File'
        'New'⎕WC'MenuItem' 'New'
        'Open'⎕WC'MenuItem' 'Open'
        'Close'⎕WC'MenuItem' 'Close'
    :EndWith

    :With 'Edit'⎕WC'Menu' 'Edit'
        'Cut'⎕WC'MenuItem' 'Cut'
        'Copy'⎕WC'MenuItem' 'Copy'
        'Paste'⎕WC'MenuItem' 'Paste'
    :EndWith

:EndWith
```


![](../img/tool10.gif)


