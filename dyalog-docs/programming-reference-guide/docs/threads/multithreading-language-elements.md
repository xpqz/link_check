<h1 class="heading"><span class="name">Multi-Threading Language Elements</span></h1>

The following language elements are provided to support threads.

- Primitive operator, spawn: `&`.
- System functions: `⎕TID`,  `⎕TCNUMS`,  `⎕TNUMS`,  `⎕TKILL`,  `⎕TSYNC`.
- An extension to the GUI Event syntax to allow asynchronous callbacks.
- A control structure: `:Hold`.
- System commands: `)HOLDS`, `)TID`.
- Extended `)SI` and `)SINL` display.

## Running Callback Functions as Threads

A callback function is associated with a particular event via the Event property of the object concerned. A callback function is executed by `⎕DQ` when the event occurs, or by `⎕NQ`.

If you append the character `&` to the name of the callback function in the `Event` specification, the callback function will be executed asynchronously as a thread when the event occurs. If not, it is executed synchronously as before.

For example, the event specification:
```apl
      ⎕WS'Event' 'Select' 'DoIt&'
```

tells `⎕DQ` to execute the callback function `DoIt` *asynchronously as a thread* when a Select event occurs on the object.
