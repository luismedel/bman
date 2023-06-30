# bman

A command line bookmark manager.

## Installation

> Note: you need Python 3.

```sh
> pip install bman
```

After that, should have a `bman` command available.

```sh
> bman

Usage: bman [OPTIONS] COMMAND [ARGS]...

  Your command line bookmark manager.

Options:
  -h, --help  Show this message and exit.

Commands:
  add  Adds a new entry
  ls   Lists stored entries
  rm   Removes an entry
```

## Usage

### Add a bookmark

The quickest way to add an url is:

```sh
> bman add https://google.com
```

But maybe you prefer to add a tiny description to the bookmark:

```sh
> bman add https://google.com "The google homepage"
```

Or, better, add some tags to help you organize all this mess:

```sh
> bman add https://google.com "The google homepage" search,homepage,faang
```

### List bookmarks

You can query all your bookmarks with the `ls` command:

```sh
> bman ls

https://github.com
Date: 2023-07-01T20:49:29.273570
Description: The github homepage
Tags: ['code', 'homepage', 'faang']

https://google.com
Date: 2023-07-01T20:51:49.173430
Description: The google homepage
Tags: ['search', 'homepage', 'faang']
```

Of course, once you start adding bookmarks is not feasible to get a dump of all entries every time you use `ls`. You can use a filter:

```sh
> bman ls goog

https://google.com
Date: 2023-07-01T20:51:49.173430
Description: The google homepage
Tags: ['search', 'homepage', 'faang']
```

The filter works on all fields.

Search by tag:

```sh
> bman ls search

https://google.com
Date: 2023-07-01T20:51:49.173430
Description: The google homepage
Tags: ['search', 'homepage', 'faang']
```

By date:

```sh
> bman ls 2023-07

https://github.com
Date: 2023-07-01T20:49:29.273570
Description: The github homepage
Tags: ['code', 'homepage', 'faang']

https://google.com
Date: 2023-07-01T20:51:49.173430
Description: The google homepage
Tags: ['search', 'homepage', 'faang']
```

The `ls` command accepts some more interesting options worth exploring:

```sh
Usage: bman ls [OPTIONS] [FILTER]

  Lists stored entries

Options:
  --format [only-url|full|json]  Set the output format
  --use-regex                    Treat the search filter as a regex pattern
  --fields TEXT                  Comma separated list of fields to show (and
                                 to apply filter to)
  -h, --help                     Show this message and exit.
```

### Removing bookmarks

I know, I know...you rarely delete bookmarks. Neither me. But when you need to, better to have a way to do it :-)

```sh
> bman rm http://google.com
```

And that's it.

### Editing bookmarks

`bman` doesn't allow direct edition, but you can add a bookmark twice to update it's entry:

For example, returning to the previous example, if you already had `http://google.com` in your library...

```sh
> bman add http://google.com "The _don't be evil_ company"

Url already exists in the library. Please, use --force to update it with the new values.
```

As you see, you need to pass the `--force` flag:

```sh
> bman add http://google.com "The _don't be evil_ company" --force
```

## Data location

By default `bman` stores all the data under the `~/.bman/` directory. This can be overrided setting the `BMAN_ROOT_PATH` environment variable.

Under that directory, you'll find:

- `config.json` for configuration settings (there's barely anything configurable right now, to be fair)
- `library.json` with all your bookmarks.

I chose JSON for all data representation to make it easier to work with it using standard tools, if I need to.
