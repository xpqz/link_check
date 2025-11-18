




<h1 class="heading"><span class="name">Reset State Indicator</span> <span class="command">)RESET {n}</span></h1>



This command cancels all suspensions recorded in the state indicator and discards any unprocessed events in the event queue.


The optional parameter `n` specifies that only the top `n` suspensions are to be cleared.


`)RESET` also performs an internal re-organisation of the workspace and process memory. See [Workspace Available](../system-functions/wa.md)  for details.

<h2 class="example">Example</h2>
```apl
      )SI
#.FOO[1]*
⍎
#.FOO[1]*
 
      )RESET
 
      )SI
```



