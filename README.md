# TODOTui

## Description

TODO Tui is a terminal UI for managing TODOs both globally and for a project. It is designed with simplicity in mind and for the use of a single developer on a single machine.
There is a simple configuration for managing the size of the TODO box and when integrating TODO Tui with `direnv` you can produce an automatic `todo list` whenever you CD into a project. TODO Tui has a handy `todo setup` command for setting up `direnv` for a project.

## Installation

pip install todotui

## Examples

### List todos locally, if in a git project, or global.

    ❯ todo list
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | ID |                                           Title                                            |  Created at  |  Completed  |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | 1  | Fix the auto command                                                                       | 26/01 19:49  |      ❌     |
    | 2  | Add more databases                                                                         | 26/01 19:49  |      ❌     |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+

### Add a new todo

    ❯ todo add "Book a strategy meeting"
    Created task with id: 3

    ❯ todo list
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | ID |                                           Title                                            |  Created at  |  Completed  |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | 1  | Fix the auto command                                                                       | 26/01 19:49  |      ❌     |
    | 2  | Add more databases                                                                         | 26/01 19:49  |      ❌     |
    | 3  | Book a strategy meeting                                                                    | 26/01 19:50  |      ❌     |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+

### Delete a todo

    ❯ todo delete 3
    Deleted task with id: 3

    ❯ todo list
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | ID |                                           Title                                            |  Created at  |  Completed  |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | 1  | Fix the auto command                                                                       | 26/01 19:49  |      ❌     |
    | 2  | Add more databases                                                                         | 26/01 19:49  |      ❌     |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+

### Add a global todo

    ❯ todo -g add "Book a strategy meeting"
    Created task with id: 1

    ❯ todo list -g
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | ID |                                           Title                                            |  Created at  |  Completed  |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | 1  | Book a strategy meeting                                                                    | 26/01 19:52  |      ❌     |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+

### Complete a todo

    ❯ todo -g done 1
    Task with id 1 completed

    ❯ todo -g list
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | ID |                                           Title                                            |  Created at  |  Completed  |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | 1  | Book a strategy meeting                                                                    | 26/01 19:52  |      ✅     |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+

### Automatically add todos from TODO comments in code

    ❯ todo auto
    Created 1 new tasks

    ❯ todo list
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | ID |                                           Title                                            |  Created at  |  Completed  |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+
    | 1  | Fix the auto command                                                                       | 26/01 19:49  |      ❌     |
    | 2  | Add more databases                                                                         | 26/01 19:49  |      ❌     |
    | 3  | todo/commands/auto.py:Add a docstring to this method                                       | 26/01 19:56  |      ❌     |
    +----+--------------------------------------------------------------------------------------------+--------------+-------------+

## Configuration

The configuration is stored in `$HOME/.local/state/todotui/config.yaml`, if there is no config.yaml file there just run `todo list` once and it should be created.

In the configuration it is possible to change the text alignment and size of the TODO output.
There are four segments in the TODO output that can be configured: id, title, created_at & completed and the configuration is the same for each of them.

Change the text alignment using `text.align`. Values for alignments are center='^', left='<' and right='>'

Example:

    format:
      tasks:
        title:
          text:
            align: <  # align title left

Change the title alignment using `title.align`. Values for alignments are center='^', left='<' and right='>'

Example:

    format:
      tasks:
        id:
          title:
            align: <  # align title left

Change the header of a box using `title.text`.

Example:

    format:
      tasks:
        title:
          title:
            text: Name

Change the width of a box using `width`, the width is the total number of characters.

Example:

    format:
      tasks:
        id:
          width: 4

To restore the default configuration just delete the configuration file at `$HOME/.local/state/todotui/config.yaml` and it will be recreated the next time you run the program.

## Contribute

- Issue Tracker: https://github.com/TP-Softworks/todotui/issues
- Source Code: https://github.com/TP-Softworks/todotui

## Support

Please open an issue: https://github.com/TP-Softworks/todotui/issues
or start a discussion: https://github.com/TP-Softworks/todotui/discussions/categories/q-a
