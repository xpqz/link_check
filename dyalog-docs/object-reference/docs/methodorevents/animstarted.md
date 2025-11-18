<h1 class="heading"><span class="name">AnimStarted</span> <span class="right">Event 294</span></h1>



**Applies To:** [Animation](../objects/animation.md)

**Description**


If enabled, this event is reported by an [Animation](../objects/animation.md) object just before an AVI clip starts playing


The event message reported as the result of `⎕DQ`, or supplied as the right argument to your callback function, is a 2-element vector as follows :


|-----|------|-----------------------|
|`[1]`|Object|ref or character vector|
|`[2]`|Event |`'AnimStarted'` or 294 |


This event is reported for information only and cannot be disabled or modified in any way.



