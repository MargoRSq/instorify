# Dream Renovation

## Sections
1. [Links](#links)
1. [Requirements](#requirements)
1. [Install](#install)
1. [Start developing](#start-developing)
1. [Scripts flags](#scripts-flags)
1. [Structure](#structure)
1. [Developing steps](#developing-steps)
    * [Branches](#branches)
    * [Commits](#commits)
        * [Examples](#examples)
    * [Pull Requests](#pull-requests)
1. [Build](#build)
1. [Start app](#start-app)
1. [Deploy](#deploy)

## Links

### Site urls:

Previw (Heroku): https://instorify-api.herokuapp.com/

### Requirements:

Python 3.9 required

* **TODO**

## Install

```bash
pipenv install --dev
```
or if you don't want to use pipenv and want to store dependencies in project dir
```bash
pip install virtualenv --upgrade
python -m venv env/
cd env/Script
activate.bat
cd ../../
pip install -r requirements.txt
```

## Start developing

Start uvicorn server with API using these commands:
```bash
pipenv shell
cd app/
uvicorn main:app
```
This starts the development server on http://localhost:8000.


## Scripts flags

|`uvicorn main:app <flag>`    |Description|
|-------------------|-----------|
|`--reload`         |Run app with auto-reload|
|`--env-file PATH`  |Run app with env-variables from PATH|
|`--log-config PATH`|Run app with logging in log from PATH|

## Structure

```
├───app
│   │   main.py     # file with main API app that uvicorn running
│   ├───api         # dir with api routes and parse-plugins
│   │   └───routes
│   │       │   api.py          # main API router, that includes all routes with prefix
│   │       ├───dependencies    # dependencies for api endpoints
│   │       └───inst            # instagram routes
│   ├───plugins
│   |   └───instagram           # instagram parse-plugins
│   |       └───clients         # instagram web_api and private_api auth
│   ├───models         # schemas and database models
│   |   └───instagram
│   |       └───schemas         # schemas with requests and response models
└───cache       # cookie files with applications auth

```

## Developing steps

* **TODO**

### Branches

The process of adding new functionality begins by creating a new branch for development, branching from the `develop` branch. The name prefix for the branch is selected based on the type of added functionality:

* `feat` ─ adding new user features
* `fix` ─ fixing bugs
* `chore` ─ adding / updating new features that with doesn't affect user code. Example, optimizing package builds, code rules and etc
* `docs` - documentation

Then comes the `/` character and a short associative name in `kebab-case`.

So, for example, the name of the branch for adding the change new header may have the name: `feat/new-header`.

### Commits

Comments to commits are formatted to the following rule:

```
<type>(<scope>): <subject>
```

#### Type

* `feat` - using for adding new feature
* `fix` - fixing some bug
* `docs` - add or update docs
* `test` - add or update tests for app
* `chore` - optimizing package builds, code rules and etc

#### Scope

Here you must specify which areas were affected commit. Example: `(header)` or `(button)`

#### Subject

Common style message:

```
action (with lower case) + for which entity + (optional details)
```

For example:
```
fix margin in button
```

#### Examples

```
feat(footer): add phone in contact
fix(modal): fix shadow for modal
chore(next-config): add rewrite for redirect in next config
```

### Pull Requests

The development process ends with a Pull Request of the development branch in the `develop` branch on [github.com](https://github.com/MargoRSq/instify).
* If the `develop` branch has gone ahead during development, it is necessary to `rebase` from it.

## Build

* **TODO**

## Start app

* **TODO**

## Deploy

* **TODO**
