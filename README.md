# create-litestar

Easy way to start a Litestar project

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="media/litestar-framework-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="media/litestar-framework-light.svg">
  <img alt="Litestar framework banner" src="media/litestar-framework-light.svg">
</picture>

## Quick start

Head over to [litestar.dev](https://litestar.dev/templates) to get started quickly.

## Usage

You can use the `create-litestar` CLI to clone the latest template to an empty directory:

```sh-session
$ uvx create-litestar@latest [<dir>] [-t,--template=<template>]
```

**Example:** Clone `plugin` to `my-app` directory:

```sh-session
$ uvx create-litestar@latest my-app -t plugin
```

## Templates

Name | Description | Command   |
-----|-------------|-----------|
[Litestar](https://github.com/Kumzy/templates/templates/litestar) | Starter for an API | `uvx create-litestar@latest -t litestar` |
[Plugin](https://github.com/Kumzy/templates/templates/plugin) | Starter for a plugin | `uvx create-litestar@latest -t plugin` |
[Middleware](https://github.com/Kumzy/templates/templates/middleware) | Starter for a middleware| `uvx create-litestar@latest -t middleware` |

## Development

```bash
uv sync
```
