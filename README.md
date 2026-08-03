# dnstool

A CLI tool for forward and reverse DNS lookups. Queries both your local (internal) resolver and an external nameserver side by side so you can compare results.

## Features

- **Forward lookups** — queries A, AAAA, MX, TXT, NS, CNAME, and SOA records for a given hostname
- **Reverse lookups** — resolves IP addresses (IPv4 and IPv6) to hostnames via PTR records
- **Dual resolution** — runs each lookup against both your internal resolver and an external one (default: 8.8.8.8)

## Installation

```bash
pip install .
```

Or build a wheel and install it anywhere:

```bash
uv build
pip install dist/dnstool-0.1.0-py3-none-any.whl
```

## Usage

**Look up a hostname:**

```bash
dnstool example.com
```

**Reverse look up an IP address:**

```bash
dnstool 8.8.8.8
```

**Specify a different external nameserver:**

```bash
dnstool example.com --nameserver 1.1.1.1
```

## Requirements

- Python >= 3.11
- [dnspython](https://www.dnspython.org/) >= 2.8.0
