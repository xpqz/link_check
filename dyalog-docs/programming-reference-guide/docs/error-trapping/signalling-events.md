<h1 class="heading"><span class="name">Signalling Events</span></h1>

It would be useful to be able to employ the idea of cutting back the stack and taking an alternative route through the code, when a condition other than an APL error occurs. To achieve this, we must be able to trap on errors other than APL errors, and we must be able to define these errors to APL. We do the former by using error codes in the range 500 to 999, and the latter by using `⎕SIGNAL`.

Consider our system; ideally, when an unexpected error occurs, we want to save a snapshot copy of our workspace (execute `BUG` in place), then immediately jump back to `REPORT` and reduce our options. We can achieve this by changing our functions a little, and using `⎕SIGNAL`:

```apl
      ∇ REPORT;OPTIONS;OPTION;⎕TRAP
   [1] ⍝ Driver functions for report sub-system. If an
   [2] ⍝ unexpected error occurs, make a snapshot copy
   [3] ⍝ of the workspace, then cutback the stack to
   [4] ⍝ this function, reduce the option list & resume
   [5] ⍝ Set global trap
   [6]  ⎕TRAP←(500 'C' '→ERR')(0 'E' 'BUG')
   [7] ⍝ Available options
   [8]  OPTIONS←'REP1' 'REP2' 'REP3' 'REP4'
   [9] ⍝ Ask user to choose
  [10] LOOP:→END×⍳0=⍴OPTION←MENU OPTIONS
  [11] ⍝ Execute relevant function
  [12]  ⍎OPTION
  [13] ⍝ Repeat until EXIT
  [14]  →LOOP
  [15] ⍝ Tell user ...
  [16] ERR:MESSAGE'Unexpected error in',OPTION
  [17] ⍝ ... what's happening
  [18]  MESSAGE'Removing from list'
  [19] ⍝ Remove option from list
  [20]  OPTIONS←OPTIONS~⊂OPTION
  [21] ⍝ And repeat
  [22]  →LOOP
  [23] ⍝ End
  [24] END:
```
```apl
       ∇ BUG
   [1] ⍝ Called whenever there is an unexpected error
   [2]   '*** UNEXPECTED ERROR OCCURRED IN: ',⊃1↓⎕SI
   [3]   '*** PLEASE CALL YOUR SYSTEM ADMINISTRATOR'
   [4]   '*** WORKSPACE SAVED AS BUG.',⊃1↓⎕SI
   [5]   ⍝ Tidy up ... reset ⎕LX, untie files ... etc
   [6]   ⎕SAVE 'BUG.',⊃1↓⎕SI
   [7]   '*** RETURNING TO DRIVER FOR RESELECTION'
   [8]   ⎕SIGNAL 500
       ∇
```

Now when the unexpected error occurs, the first trap specification catches it, and the `BUG` function is executed in place. Instead of logging the user off as before, an `error 500` is signalled to APL. APL checks its trap specifications, sees that 500 has been set in `REPORT` as a cut-back, so cuts back to `REPORT` before branching to `ERR`.

## Flow Control

Error handling, which employs a combination of all the system functions and variables described, allows us to dynamically alter the flow of control through our system, as well as allow us to handle errors gracefully. It is a very powerful facility, which is simple to use, but is often neglected.
