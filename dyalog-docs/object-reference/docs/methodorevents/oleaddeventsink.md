<h1 class="heading"><span class="name">OLEAddEventSink</span> <span class="right">Method 540</span></h1>



**Applies To:** [OCXClass](../objects/ocxclass.md), [OLEClient](../objects/oleclient.md)

**Description**


This method connects a named event sink to a COM object and adds the events defined by that event sink to the [EventList](../properties/eventlist.md) property of the associated namespace.


The argument to OLEAddEventSink is a single item as follows:


|-----|---------------|----------------|
|`[1]`|Event sink name|character vector|


The result is a number that represents the handle of the event sink. This may be subsequently required.



