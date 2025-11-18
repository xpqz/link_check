# Documentation Styles
Central respository of stylesheets used in documentation of Dyalog projects

## How to include in another project
Futher explanation in [github.blog/open-source/git/working-with-submodules/](https://github.blog/open-source/git/working-with-submodules/).

These styles are for inclusion in Dyalog project that use [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for their documentation to enforce a consistent style and allow updating styles from a single source.

1. Clone the repository for the project.
2. Open a terminal (with Git installed) and navigate (`cd`) to the directory **docs/style**.
3. Run the following command to add this repository as a Git submodule.
    ```shell
    git submodule add https://github.com/Dyalog/documentation-styles
    ```