<h1 class="heading"><span class="name">DockAccept</span> <span class="right">Event 483</span></h1>



**Applies To:** [CoolBand](../objects/coolband.md), [CoolBar](../objects/coolbar.md), [Form](../objects/form.md), [SubForm](../objects/subform.md), [ToolControl](../objects/toolcontrol.md)

**Description**


If enabled, this event is reported by a host object just before it accepts a client object docking operation. This event is reported (by the host) immediately after the [DockRequest](./dockrequest.md) is reported (by the client).


The event message reported as the result of `⎕DQ`, or supplied as the right argument to your callback function, is a 7-element vector as follows :


|-----|-----------------|-----------------------|
|`[1]`|Object           |ref or character vector|
|`[2]`|Event            |`'DockAccept'` or 483  |
|`[3]`|Client Object    |ref or character vector|
|`[4]`|Edge             |character vector       |
|`[5]`|y-position       |number                 |
|`[6]`|x-position       |number                 |
|`[7]`|Outline rectangle|4-element nested       |


Elements 4-7 of this event message are the same as those reported by [DockMove](./dockmove.md), and the effect of a callback function is identical. See [DockMove](./dockmove.md) for further information.



