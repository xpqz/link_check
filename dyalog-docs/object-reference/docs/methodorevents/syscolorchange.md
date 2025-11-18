<h1 class="heading"><span class="name">SysColorChange</span> <span class="right">Event 134</span></h1>



**Applies To:** [Root](../objects/root.md)

**Description**


If enabled, this event is reported when the user or another application updates the system colour palette. The event is reported after the change has taken place and cannot be disabled or inhibited in any way. If you want your application to respond to colour palette changes, this event gives you the opportunity of doing so.


The event message reported as the result of [`⎕DQ`](../../../language-reference-guide/system-functions/dq), or supplied as the right argument to your callback function, is a 2-element vector as follows :


|-----|------|-------------------------|
|`[1]`|Object|ref or character vector  |
|`[2]`|Event |`'SysColorChange'` or 134|



