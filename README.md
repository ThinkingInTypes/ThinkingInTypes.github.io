# Thinking in Types

## Building Stubbornly Resilient Python Code

[ThinkingInTypes.com](https://thinkingintypes.com/)

## By Bruce Eckel

- Run locally: `mkdocs serve`
- Deploy: `mkdocs gh-deploy`

## Running `prettier` to format Markdown

- `npx prettier --write .` Reformats in-place all files in current directory
- `npx prettier --write .\04_Using_Types.md` Just reformats that file

## Tools

- `uvx mdformat`  Formats fenced code blocks in Markdown files
- `docker run -v ${PWD}:/data ghcr.io/bobheadxi/readable fmt *`  Formats Markdown files including [Semantic Line Breaks](https://sembr.org/)
- [sembr](https://github.com/admk/sembr) Just does semantic line breaks using AI, but it also breaks at clauses rather than just sentences.

## Type Checker

- https://pyre-check.org/ Pyre, only works on Linux/Unix

[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/).

## TODO

- Test on Linux Subsystem for Windows
- Tooling should allow easy round-trip update of an individual file, also easy insertion of a single code example
