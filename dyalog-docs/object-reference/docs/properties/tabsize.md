<h1 class="heading"><span class="name">TabSize</span> <span class="right">Property</span></h1>



**Applies To:** [TabControl](../objects/tabcontrol.md)

**Description**


The TabSize property specifies the size of fixed size tabs or buttons in a TabControl object.


By default, the size of the tabs may vary from one to another. Fixed size tabs may be obtained by setting the TabSize property.


TabSize is a 2-element numeric vector that specifies the height and width of the tab. The first element of TabSize may be set to `⍬` which means "default height".


To obtain fixed sized tabs with [MultiLine](multiline.md) set to 1, you must however also set the Justify property to `'None'`.


If [MultiLine](multiline.md) is 1 and Justify is `'Right'`, TabSize is ignored.



