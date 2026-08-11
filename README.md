# litestar-create

Easy way to start a Litestar project

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Kumzy/litestar-create/main/media/litestar-framework-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Kumzy/litestar-create/main/media/litestar-framework-light.svg">
  <img alt="Litestar framework banner" src="https://raw.githubusercontent.com/Kumzy/litestar-create/main/media/litestar-framework-light.svg">
</picture>

## Quick start

Head over to [litestar.dev](https://litestar.dev/templates) to get started quickly.

## Usage

Run the CLI and pick a template interactively:

```sh-session
$ uvx litestar-create@latest
```

Or scaffold non-interactively by passing a project name and a template:

```sh-session
$ uvx litestar-create@latest [<name>] [-t,--template=<template>] [--list]
```

**Example:** Scaffold the `plugin` template into a `my-app` directory:

```sh-session
$ uvx litestar-create@latest my-app -t plugin
```

All available options are listed by `--help`:

```sh-session
$ litestar-create --help
usage: litestar-create [-h] [-t TEMPLATE] [--list] [name]

Create a new Litestar project

positional arguments:
  name                  Name of the new project

options:
  -h, --help            show this help message and exit
  -t, --template TEMPLATE
                        Template to scaffold from
  --list                List the available templates and exit
```

## Templates

Templates are pulled from the
[litestar-templates](https://github.com/Kumzy/litestar-templates) repository.
Run `litestar-create --list` to see the available templates.

## Development

```bash
uv sync --all-groups   # plain `uv sync` skips the test and lint groups
make test
make lint
```
