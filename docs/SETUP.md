# BrokerGuard Setup Guide

This guide walks you through local setup, Docker broker profiles, and scan execution.

## 1) Prerequisites

- Python 3.10+
- Docker + Docker Compose
- macOS/Linux shell (zsh/bash)

## 2) Clone and enter project

```bash
cd BrokerGuard
```

## 3) Install dependencies

```bash
make install
source .venv/bin/activate
```

If you prefer manual install:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4) Start the MQTT lab

### Option A: Insecure profile (for failing checks)

```bash
make up-insecure
```

### Option B: Hardened profile (for passing checks)

Before running hardened mode:

1. Generate password file:

```bash
cd docker
docker run --rm -it -v "$PWD/secrets:/secrets" eclipse-mosquitto:2 mosquitto_passwd -c /secrets/passwords.txt student
cd ..
```

2. Add certificates to `docker/certs/`:

- `ca.crt`
- `server.crt`
- `server.key`

Then start:

```bash
make up-hardened
```

## 5) Run scanner

Text output:

```bash
make scan
```

JSON output:

```bash
make scan-json
```

Direct Python commands also work:

```bash
python brokerguard.py
python brokerguard.py --json
```

## 6) Run tests

```bash
make test
```

## 7) Stop lab and clean project artifacts

Stop containers:

```bash
make down
```

Clean virtual environment, logs, and cache files:

```bash
make clean
```
