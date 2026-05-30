# List recipes
default:
  just --list

# run the hugo dev server
up:
  hugo server --buildDrafts --buildFuture

# create a new post with the given name (converts to kebab-case)
new name:
  #!/usr/bin/env bash
  fmt_name=$(echo "{{name}}" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
  hugo new post/${fmt_name}/index.md
