---
date: 2019-09-18 20:13:56+01:00
description: ''
draft: false
externalUrl: ''
isStarred: false
title: Empty Git Commits
---
Some build pipelines have steps which are only triggered if a certain phrase is contained in the commit message. The problem is sometimes e.g. after a code review there may be nothing to commit but you need to start this build process.

Try doing an empty commit in VS Code and a warning message says "there are no changes to commit".

The solution when you need an empty commit is to use the allow empty flag and add the commit message you need:

```bash
git commit --allow-empty -m "[magic build]"
```

In the example above the string `[magic build]` triggers additional steps in the CI build. Problem solved.
