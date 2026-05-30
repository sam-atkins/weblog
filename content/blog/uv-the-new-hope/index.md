---
date: '2024-09-24 19:09:11'
description: ''
draft: false
externalUrl: "https://astral.sh/blog/uv-unified-python-packaging"
isStarred: false
title: uv - the new hope?
---
I'm genuinely excited about `uv`, a new package manager and more for Python, from the creators and maintainers of `ruff`. `uv` started as a `pip` alternative and has now expanded to become closer to their aspiration of being Cargo (the Rust package manger) for Python.

Firstly, what excites me about uv is it has the potential to be one tool that replaces many. It has functionality to be an alternative to `pip`, `poetry`, `pipx` and `pyenv`.

Secondly, the speed of `uv` is incredible.

Last, and by no means least, what excites me is the workflows behind certain commands. For example:

- If you have a `uv` project e.g. you have run `uv init`, then adding a dependency will auto create a virtual env if one does not already exist, activate it and install the dependency into it. All this by running `uv add {pkg}`.
- If you invoke your script or app with `uv run` e.g. `uv run main.py` then `uv` will check the lockfile and virtualenv are consistent and run your Python code in the activated virtual env.

I think abstracting away the virtualenv like this can be really helpful to Python beginners. And I will really enjoy not having to remember some additional steps when trying to get something done.

All my personal Python projects will use `uv` from now on. I really hope it catches on and becomes *the* Python package manager.
