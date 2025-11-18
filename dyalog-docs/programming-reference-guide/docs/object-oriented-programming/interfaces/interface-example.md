<h1 class="heading"><span class="name">Penguin Class Example</span></h1>

The Penguin Class example illustrates the use of Interfaces to implement *multiple inheritance*.

[FishBehaviour Interface](fishbehaviour-interface.md){: .noprint }

[BirdBehaviour Interface](birdbehaviour-interface.md){: .noprint }

[Penguin Class](penguin-class.md){: .noprint }

In this case, the `Penguin` Class derives from `Animal` but additionally supports the `BirdBehaviour` and `FishBehaviour` Interfaces, thereby inheriting members from both.
```apl
      Pingo←⎕NEW Penguin
      ⎕CLASS Pingo
  #.Penguin  #.FishBehaviour  #.BirdBehaviour    #.Animal
 
      (FishBehaviour ⎕CLASS Pingo).Swim
I can dive and swim like a fish
      (BirdBehaviour ⎕CLASS Pingo).Fly
Although I am a bird, I cannot fly
      (BirdBehaviour ⎕CLASS Pingo).Lay
I lay one egg every year          
      (BirdBehaviour ⎕CLASS Pingo).Sing
Croak, Croak!           
```
