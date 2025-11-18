<h1 class="heading"><span class="name">Detach</span> <span class="right">Method 270</span></h1>

[**Applies To**](../methodoreventapplies/detach.md)

**Description**


This method is used to detach the GUI component from an object without losing the functions, variables and sub-namespaces that it may contain.


The Detach method is niladic.


The effect of this method is to remove the GUI component associated with the named object, leaving behind a plain namespace of the same name. All non-GUI child objects are retained. GUI child objects are either destroyed, or similarly converted to plain namespaces depending upon the values of their KeepOnClose properties.



