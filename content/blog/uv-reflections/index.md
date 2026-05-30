---
title: "uv reflections"
date: 2025-08-09T08:35:09+01:00
draft: false
description:
isStarred: false
externalUrl:
---
Sometime ago, I wrote about my hopes for [`uv`](https://samatkins.co/post/uv-the-new-hope/). It has surpassed my expectations. There isn't always the time to migrate old projects at work, but for all future projects I by default reach for `uv`.

What I love is it has brought a "Cargo" like packaging experience to Python. Additions like `uv run` and `uvx` are also really useful.

The game change for me is `uv venv`. I no longer have to worry or care about installing different versions of Python. If I need to work on an older version of Python `uv venv --python 3.10`  will do the job, need a newer version `uv venv --python 3.13`. You get the idea.

What's beautiful is if a Python version isn't on my machine, `uv venv` will download and install it. The `uv venv` command has not only replaced my usage of the `venv` tool but also Python version management tools like `pyenv`.

`uv` is a great tool and another success from the team at Astral.
