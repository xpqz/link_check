




<h1 class="heading"><span class="name">FILE INDEX ERROR</span> <span class="command">20</span></h1>



This report is given when an attempt is made to reference a non-existent component.

<h2 class="example">Example</h2>
```apl
      ⎕FSIZE 1
1 21 16578 4294967295
 
      ⎕FREAD 1 34
FILE INDEX ERROR
      ⎕FREAD 1 34
      ^
      ⎕FDROP 1 50
FILE INDEX ERROR
      ⎕FDROP 1 50
      ^
```



