




<h1 class="heading"><span class="name">FILE NAME ERROR</span> <span class="command">22</span></h1>



This report is given if:

- the user attempts to `⎕FCREATE` using the name of an existing file.
- the user attempts to `⎕FTIE` or `⎕FSTIE` a non-existent file, or a file that is not a component file.
- the user attempts to `⎕FERASE` a component file or `⎕NERASE` a native file with a name other than the EXACT name that was used when the file was tied.



