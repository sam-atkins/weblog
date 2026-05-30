---
title: "New Tooling in 2025"
date: 2025-11-12T06:37:40Z
draft: false
description:
isStarred: false
externalUrl:
---
I read a blog about the tools someone uses and this prompted the idea to write what I use. OK, I'm shamelessly copying the idea of writing about the tools I use day to day. (I can't remember where I saw it but if I find it, I will add a link to it here.)

After several years of using the same old tools day in and day out, what surprised me this year is not just the new tools I use but how my typical day writing code has changed. AI coding agents getting good is the reason for this.

Enough of an intro, here are the tools I use at work for software development.

## [Claude Code](https://www.anthropic.com)

Let's start with a tool which has fundamentally changed how I work and the tools I now use.

Claude Code is an AI tool that for me lives up to the hype. It isn't perfect but I consider it an invaluable tool that I use everyday in my job. Claude works away in the background until I'm notified (via a hook) that requires my input. I review and may edit the diff in my IDE and either continue coding from there or go back with another prompt to let Claude continue.

## [Ghostty](https://ghostty.org)

I liked iTerm. I liked the idea of Warp but wanted more granular control over settings, config and so on.

Ghostty is a super fast terminal, with zero config required... but if you do want to configure it (like I did), it can be done in a config file. Perfect for adding to however you manage dotfiles and configuration.

I can add things like [`atuin`](https://atuin.sh) for shell history and [Fish shell](https://fishshell.com) for 90s goodness. I held off switching to Fish for so long, I was so invested in my bash dotfiles and aliases etc. But so glad I made the switch, so much easier to work with.

## [Zellij](https://zellij.dev)

For those missing features in Ghostty (like search), then Zellij is the perfect companion. An easier onboarding experience than tmux. I'm super happy with Zellij. I have custom layouts for my dev work, with split panes with e.g. Lazydocker or Claude Code autoloaded.

## [jj](https://jj-vcs.github.io/jj/latest/)

I've been using Jujutsu Version Control System aka `jj` since the start of the year and I love it. No more trying to work out arcane git magic. A simple, consistent UI, yet just as powerful as `git`.  It took me awhile to get my head around it but now I would not go back to vanilla `git`.

## [Zed](https://zed.dev)

I'm amazed that my IDE is not as important as other dev tooling. It was always number one on my list. That's how much Claude Code has changed my ways of working.

I was a long time user of VS Code and before that Sublime Text. Zed reminds me of Sublime with its responsiveness. It's a clean UI, packed with functionality. When they launched the debugger that was when I could make the full time switch from VS Code. I would use this editor alone for the Subtle Mode when using Edit Predictions.

It's a great IDE. Typically these days I use to review a diff from Claude and do some light editing before either giving another prompt or committing the code.

## [Obsidian](https://obsidian.md)

My goto for note taking. The sync service is fantastic at syncing between my laptop and my phone. I keep all my notes here, from work to life to study. A great product.

## [Antinote](https://antinote.io)

I love Obsidian but sometimes I just need scratch notes that are quick to hand. This is where Antinote shines. And if a scratch note does need to be saved it is easy to export it to Obsidian.
