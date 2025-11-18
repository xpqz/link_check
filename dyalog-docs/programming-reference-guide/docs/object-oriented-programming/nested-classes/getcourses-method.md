---
search:
  exclude: true
---

<h1 class="heading"><span class="name">GetCourses Method</span></h1>

```apl

    ∇ R←GetCourses;COURSECODES;COURSES;INDEX
      :Access Public
      COURSECODES COURSES INDEX←⎕FREAD GOLFID 1
      R←{⎕NEW GolfCourse ⍵}¨↓⍉↑COURSECODES COURSES
    ∇
```
