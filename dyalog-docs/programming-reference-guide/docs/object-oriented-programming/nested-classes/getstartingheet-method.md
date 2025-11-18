---
search:
  exclude: true
---

<h1 class="heading"><span class="name">GetStartingheet Method</span></h1>

```apl
    ∇ R←GetStartingSheet ARGS;CODE;COURSE;DATE;COURSECODES
                             ;COURSES;INDEX;COURSEI;IDN
                             ;DATES;COMPS;IDATE;TEETIMES
                             ;GOLFERS;I;T
      :Access Public
      CODE DATE←ARGS
      COURSECODES COURSES INDEX←⎕FREAD GOLFID 1
      COURSEI←COURSECODES⍳CODE
      COURSE←⎕NEW GolfCourse(CODE(COURSEI⊃COURSES,⊂''))
      R←⎕NEW StartingSheet(0 COURSE DATE)
      :If COURSEI>⍴COURSECODES
          R.Message←'Invalid course code'
          :Return
      :EndIf
      IDN←2 ⎕NQ'.' 'DateToIDN',DATE.(Year Month Day)
      DATES COMPS←⎕FREAD GOLFID,COURSEI⊃INDEX
      IDATE←DATES⍳IDN
      :If IDATE>⍴DATES
          R.Message←'No Starting Sheet available'
          :Return
      :EndIf
      TEETIMES GOLFERS←⎕FREAD GOLFID,IDATE⊃COMPS
      T←DateTime.New¨(⊂DATE.(Year Month Day)),¨↓[1]
                                   24 60 1⊤TEETIMES
      R.Slots←{⎕NEW Slot ⍵}¨T,∘⊂¨↓GOLFERS
      R.OK←1
    ∇
```
