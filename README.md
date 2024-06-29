# FastType

## About

lib:

- FastAPI (Websockets, uvicorn)

Fast, simple typing test in FastAPI

## Install

Clone repo:

```bash
git clone https://github.com/ZeroNiki/FastTyping.git
```

go to `FastTyping`.

Create venv:

if Linux:

```bash
python -m venv venv

source venv/bin/activate
```

if Windows:

```
python -m venv venv

venv\bin\activate
```

install requirements:

```
pip install -r requirements.txt
```

## Usage

start webapp using uvicorn:

```
uvicorn src.main:app --reload
```

go to 'http://127.0.0.1:8000/pages/s'.
