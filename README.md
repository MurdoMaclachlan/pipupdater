# pipupdater

This is a small command-line tool designed for automatically updating pip packages based on the output of the pip-check module. The basic functionality is to pipe the output of `pip list --outdated --format=columns` to the `pipupdater` file, which will then attempt to extract the package names from the output and update all the modules.

This tool doesn't account for dependency conflicts and doesn't yet have any functionality for tracking what dependencies pip might have updated or installed itself. At the moment, it's very barebones due to being written in about half an hour by someone who was sicking of having to manually update each pip package.

## Requirements & installation

Currently there is no setup file for this tool, but that's on the list. It depends on the `pip-check` module, which you can install through pip. I set it up by putting a symbolic link from where I have the git repo saved to my `~/.local/bin` folder. When I want to run it, I just do:

    pip list --outdated --format=columns | pipupdater

(Actually, I have it aliased to `pipupdateall`. Same difference.)

## Roadmap

Here's a list of things I plan to add or at least look into adding:

- [ ] Include dependencies pip installs/updates in log of updated packages
- [ ] A log message when no packages need updated (at the moment it just looks like nothing happened)
- [ ] A proper setup file
- [ ] Allow running as a single command
- [ ] Properly capture & hide terminal output from pip commands
- [ ] User config options
- [ ] Dependency conflict management? (maybe) (possibly)