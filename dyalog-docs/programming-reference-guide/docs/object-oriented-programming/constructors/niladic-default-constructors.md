<h1 class="heading"><span class="name">Niladic (Default) Constructors</span></h1>

A Class may define a niladic Constructor and/or one or more Monadic Constructors. The niladic Constructor acts as the default Constructor that is used when `⎕NEW` is invoked without arguments and when APL needs a [fill item](../../introduction/arrays/prototypes-and-fill-items.md).
```apl
:Class Bird
    :Field Public Species
    
    ∇ egg spec
      :Access Public Instance
      :Implements Constructor
      Species←spec
    ∇
    ∇ default
      :Access Public Instance
      :Implements Constructor
      Species←'Default Bird'
    ∇
    ∇ R←Speak
      :Access Public
      R←'Tweet, tweet!'
    ∇
    
:EndClass ⍝ Bird
```

The niladic Constructor (in this example, the function `default`) is invoked when `⎕NEW` is called without Constructor arguments. In this case, the Instance created is no different to one created by the monadic Constructor `egg`, except that the value of the `Species` Field is set to `'Default Bird'`.
```apl
      Birdy←⎕NEW Bird
      Birdy.Species
Default Bird
```

The niladic Constructor is also used when APL needs to make a [fill item](../../introduction/arrays/prototypes-and-fill-items.md) of the Class. For example, in the expression `(3↑Birdy)`, APL has to create two [fill items](../../introduction/arrays/prototypes-and-fill-items.md) of `Birdy` (one for each of the elements required to pad the array to length 3) and will in fact call the niladic Constructor twice.

In the following statement:
```apl
      TweetyPie←3⊃10↑Birdy
```

The `10↑` (temporarily) creates a 10-element array comprising the single entity `Birdy` padded with 9 fill-elements of Class `Bird`. To obtain the 9 fill-elements, APL calls the niladic Constructor 9 times, one for each separate prototypical Instance that it is required to make.
```apl
      TweetyPie.Species
Default Bird
```
