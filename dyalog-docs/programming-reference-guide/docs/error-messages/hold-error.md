




<h1 class="heading"><span class="name">HOLD ERROR</span> <span class="command">12</span></h1>



This report is given when an attempt is made to save a workspace using the system function `⎕SAVE` if any external arrays or component files are currently held (as a result of a prior use of the system function `⎕FHOLD`).

<h2 class="example">Example</h2>
```apl
      ∇HOLD∆SAVE
[1]    ⎕FHOLD 1
[2]    ⎕SAVE 'TEST'
      ∇
 
      'FILE' ⎕FSTIE 1
 
      HOLD∆SAVE
HOLD ERROR
HOLD∆SAVE[2] ⎕SAVE'TEST'
             ^
```



