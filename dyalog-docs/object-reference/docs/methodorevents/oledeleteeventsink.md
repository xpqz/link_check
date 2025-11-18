<h1 class="heading"><span class="name">OLEDeleteEventSink</span> <span class="right">Method 541</span></h1>



**Applies To:** [OCXClass](../objects/ocxclass.md), [OLEClient](../objects/oleclient.md)

**Description**


This method disconnects a named event sink from a COM object and removes the events defined by that event sink from the [EventList](../properties/eventlist.md) property of the associated namespace.


This method may be used to remove an event sink that was established automatically when the OLE object was created.


The argument to OLEDeleteEventSink is a single item as follows:


|-----|---------------|----------------|
|`[1]`|Event sink name|character vector|



