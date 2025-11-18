# The Language Bar

This directory contains the source and tooling to generate the header file for the language bar on Microsoft Windows.

To add a new entry to the language bar, compose the text as a file in the "elements" folder. These are XHTML:

```xml
<?xml version="1.0" encoding="utf-8"?>
<html conditions="HAS_UNICODE">

<head>
    <title>Jot Underbar</title>
    <char>⍛</char>
</head>

<body>
    <pre>Dyadic operator (f⍛g): Behind

Monadic: f⍛g y is evaluated as (f y) g y

      -⍛, 4  ⍝ 
¯4 4

      ⊂⍤⍋⍛⌷ 3 1 4 1 5 9 2 6  ⍝ Sort
1 1 2 3 4 5 6 9

Dyadic: x f⍛g y is evaluated as (f x) g y

      3 -⍛, 4
¯3 4

      8 ⍳⍛∊ 1 2 3 5
1 1 1 0 1 0 0 0
</pre>
</body>

</html>
```

Now add a reference to the new file in the `toc.json` file. This defines the ordering. The entries marked `blank` denotes a new section:

```json
[
    {
        "title": "Left Arrow",
        "link": "elements/Left Arrow.htm"
    },
    {
        "title": "blank"
    },
    {
        "title": "Plus",
        "link": "elements/Plus.htm"
    },
```

## Deploy

To generate the header file, run `python make-language-bar.py` in this folder. It should generate a file `elements.h`. This needs to be commited to the documentation svn repository, from where Jenkins will pick it up.