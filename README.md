# Thinking in Types

## Building Stubbornly Resilient Python Code

[ThinkingInTypes.com](https://thinkingintypes.com/)

## By Bruce Eckel

- Run locally: `mkdocs serve`
- Deploy: `mkdocs gh-deploy`

## Tools

- `uvx mdformat`  Formats fenced code blocks in markdown files
- `docker run -v ${PWD}:/data ghcr.io/bobheadxi/readable fmt *`  Formats Markdown files including [Semantic Line Breaks](https://sembr.org/)
- [sembr](https://github.com/admk/sembr) Just does semantic line breaks using AI, but it also breaks at clauses rather than just sentences.

[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/).


## Installing `prettier`

1. Check if you have a package.json file at all. If not, create one:

`npm init -y`
This creates a minimal package.json.

2. Install Prettier v2 correctly as a dev dependency
Now that you have a package.json:

`npm install --save-dev prettier@2`

Verify that it’s added:

`Get-Content .\package.json | Select-String "prettier"`

```
"devDependencies": {
  "prettier": "^2.8.8"
}
```

3. Re-run using only the local version
npx --no-install prettier --version

✅ Output should be:
`2.8.8`
