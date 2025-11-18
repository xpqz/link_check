




<h1 class="heading"><span class="name">List Classes</span> <span class="command">)CLASSES</span></h1>



This command lists the names of APL Classes in the active workspace.

<h2 class="example">Example</h2>
```apl
      )CLEAR
clear ws
      )ED ○MyClass
 
:Class MyClass
    ∇ Make Name
      :Implements Constructor
      ⎕DF Name
    ∇
:EndClass ⍝ MyClass
 
      )CLASSES
MyClass
      )COPY OO YourClass
.\OO saved Sun Jan 29 18:32:03 2006
      )CLASSES
MyClass YourClass
      ⎕NC 'MyClass' 'YourClass'
9.4 9.4
```



