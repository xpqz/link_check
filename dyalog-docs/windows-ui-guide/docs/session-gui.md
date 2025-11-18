<h1 class="heading"><span class="name">The Session GUI Hierarchy</span></h1>

As distributed, the Session object `⎕SE` contains two CoolBar objects. The first, named `⎕SE.cbtop` runs along the top of the Session window and contains the toolbars. The second, named `⎕SE.cbbot`, runs along the bottom of the Session windows and contains the statusbars.

The menubar is implemented by a MenuBar object named `⎕SE.mb`.

The toolbars in `⎕SE.cbtop` are implemented by four CoolBand objects, `bandtb1`, `bandtb2`, `bandtb3` and `bandtb4` each containing a ToolControl named `tb`.

The statusbars in `⎕SE.cbbot` are implemented by two CoolBand objects, `bandtb1` and `bandtb2`, each containing a StatusBar named `sb`.
