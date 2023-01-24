# instorify

## Sections
- [instorify](#instorify)
  - [Sections](#sections)
    - [Requirements:](#requirements)
  - [📦 Installation](#-installation)
  - [⚡Usage](#usage)
  - [Structure](#structure)


### Requirements:
 - Python3.10 or higher

## 📦 Installation

```bash
poetry install
```

## ⚡Usage
Start uvicorn server with API using this command:
```bash
poetry run python3 main.py
```
This starts the development server on http://localhost:8000.



## Structure

```
├── app
│   ├── api
│   │   ├── errors
│   │   │   ├── exceptions_handlers.py
│   │   │   └── instagram.py
│   │   └── routes
│   │       ├── api.py
│   │       ├── dependencies
│   │       └── inst
│   │           ├── api.py
│   │           ├── highlights.py
│   │           ├── posts.py
│   │           ├── stories.py
│   │           └── users.py
│   ├── core
│   │   └── config.py
│   ├── main.py
│   ├── models
│   │   └── schemas
│   │       └── instagram.py
│   └── plugins
│       └── instagram
│           ├── clients
│           │   ├── private_api.py
│           │   ├── utils.py
│           │   └── web_api.py
│           ├── highlights.py
│           ├── posts.py
│           ├── stories.py
│           ├── users.py
│           └── utils.py
```
