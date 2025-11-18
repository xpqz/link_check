




<h1 class="heading"><span class="name">While Statement</span> <span class="command">:While bexp</span></h1>



[Formal Definition](while-statement-definition.md){: .noprint }


The simplest `:While` loop is :
```apl
[1]   I←0
[2]   :While I<100
[3]       expr1
[4]       expr2
[5]       I←I+1
[6]   :EndWhile
```


Unless `expr1` or `expr2` alter the value of `I`, the above code will execute lines `[3-4]` 100 times.  This loop has a single condition; the value of `I`.  The purpose of the `:EndWhile` statement is solely to mark the end of the iteration.  It acts the same as if it were a branch statement, branching back to the `:While` line.


An alternative way to terminate a `:While` structure is to use a `:Until` statement.  This allows you to add a second condition.  The following example reads a native file sequentially as 80-byte records until it finds one starting with the string `'Widget'` or reaches the end of the file.

```apl
[1]   I←0
[2]   :While I<⎕NSIZE ¯1
[3]       REC←⎕NREAD ¯1 82 80
[4]       I←I+⍴REC
[5]   :Until 'Widget'≡6⍴REC
```


Instead of single conditions, the tests at the beginning and end of the loop may be defined by more complex ones using `:AndIf` and `:OrIf`.  For example:
```apl
[1]   :While 100>i
[2]   :AndIf 100>j
[3]       i j←foo i j
[4]   :Until 100<i+j
[5]   :OrIf i<0
[6]   :OrIf j<0
```


In this example, there are complex conditions at both the start and the end of the iteration.  Each time around the loop, the system tests that both `i` and `j` are less than or equal to 100.  If either test fails, the iteration stops.  Then, after `i` and `j` have been recalculated by `foo`, the iteration stops if `i+j` is equal to or greater than 100, or if either `i` or `j` is negative.


