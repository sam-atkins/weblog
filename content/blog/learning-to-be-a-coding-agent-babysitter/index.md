---
title: "Learning to Be a Coding Agent Babysitter"
date: 2025-10-18T09:50:50+01:00
draft: false
description:
isStarred: false
externalUrl:
---
The past few months I have been learning to be an [`AI coding agent babysitter`](/post/adventures-in-babysitting-coding-agents/). Sometimes it works well, sometimes less so. Overall I feel like it has been a productivity boost. The sweet spot is in areas where I have good expertise, so I can tell if the agent's output is good or not.

I'm still learning and trying to improve my babysitting skills. Here's what I've learned so far.

## Regularly clear the context
If I only had one tip, it would be this one. The key to clearing context regularly is to give really small and tightly defined tasks.

If the output isn't what I want, I might edit some files myself or give a new prompt in the current context. Typically after a maximum of three or four prompts, even if the output so far isn't what I want, I will clear the context and start over with a new prompt.

## Use planning mode
I use planning mode to explore new areas of a codebase, to research a task or investigate possible areas where there might be a bug in the code.

When planning work and I have a good output from the agent, I use a snippet to ask it to tell the agent to "write this output as a markdown file in `{dir}`. Give the file an appropriate name and start it with today's date `{date:medium}` in YYYYMMDD format".

## Use hooks
I have a hook with Claude Code that sends a notification when it needs me. For example, this users terminal-notifier on my Mac:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "terminal-notifier -message \"Claude needs your input\" -title \"Claude Code\""
          }
        ]
      }
    ]
  }
}
```

This way, if I've switched focus, I am notified and don't waste time with Claude doing nothing.

Another hook formats the code after Claude is done. This removes the need to include this in the prompt or worry about if the agent is going to ignore the instruction in the `Claude.md` to always format the code.

## Write tests yourself
Leave Claude alone to write tests and the output is usually substandard. For example lots of duplicated test cases and tests that don't even test production code. It could be a fragrant abuse of Mocks or by writing actual production code within the test and then asserting the code passes.

I will either write the tests myself, or at least the outline of the test and ask the agent to complete writing the test.

Whichever approach I go for, I always review the output. This is necessary for all code the agent writes but especially the tests. If your tests are bad, you can have even less confidence in the production code the agent writes.

## Code reviews

After I've refactored, I will often ask Claude to do a code review of the diff. I do this in plan mode so my diff won't be overwritten. It can sometimes provide some useful feedback that leads to a new prompt in a new context to refactor the code.

## Agent MD files
I find these useful for two key reasons. When I'm new to a codebase, it's a useful summary of the repo. An outline of the architecture, what is this repo about etc. Secondly, for the agent, it is useful to provide it with commands for running tests.

I've watched an agent try 3 different ways to run tests before I interrupt to remind it activate the Python venv first then run the test command. With this instruction in the Agent markdown file, this type of issue is greatly reduced.

Do these files help more than that? I'm not so sure, but I could be wrong. And all the providers always recommend it, so I still do it for every new repo I work on.

## Multiple agents in parallel

I’ve read about engineers running multiple agents with git work trees. The bottleneck for me is reviewing the output and the context switching involved in that. Running two or more implementing agents is hard mental work so I do this in limited bursts.

What I do is research or planning tasks with one agent whilst I’m working on the implementation of another. It means once I’m ready to put the implementation work into pull request, I already have some research and a draft plan ready. I can review that in more detail and then start work.

I want to experiment and iterate with this area some more so I consider this area a work in progress for me.
