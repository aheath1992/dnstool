% DNSTOOL(1) dnstool 0.1.1 | User Commands
% Andrew Heath <aheath1992@gmail.com>
% October 2026

# NAME

dnstool - look up DNS records against internal and external resolvers

# SYNOPSIS

**dnstool** \[**\-\-nameserver** *ADDRESS*] *hostname*

**dnstool** \[**\-h**|**\-\-help**]

# DESCRIPTION

**dnstool** performs a DNS lookup for *hostname* and prints the results twice:
once as resolved by the system's configured resolver (labelled *internal*), and
once as resolved by an external nameserver (labelled *external*). Running both
side by side makes it easy to spot split-horizon DNS, stale caches, or records
that differ between a private zone and the public internet.

If *hostname* parses as an IPv4 or IPv6 address, **dnstool** performs a reverse
lookup instead, querying the **PTR** record for the corresponding
*in-addr.arpa* or *ip6.arpa* name.

Otherwise a forward lookup is performed, querying the following record types:
**A**, **AAAA**, **MX**, **TXT**, **NS**, **CNAME**, and **SOA**. Record types
with no answer are omitted from the output.

# OPTIONS

**\-\-nameserver** *ADDRESS*
:   IP address of the external nameserver to query for the second lookup.
    Defaults to *8.8.8.8*.

**\-h**, **\-\-help**
:   Print a usage summary and exit.

# EXIT STATUS

**dnstool** exits 0 on success and 2 if the command line could not be parsed.
Resolution failures are reported on standard output and do not change the exit
status.

# EXAMPLES

Look up all supported records for a hostname:

    dnstool example.com

Reverse look up an IP address:

    dnstool 8.8.8.8

Compare the internal resolver against Cloudflare rather than Google:

    dnstool example.com --nameserver 1.1.1.1

# SEE ALSO

**dig**(1), **host**(1), **nslookup**(1), **resolv.conf**(5)

dnstool home page: <https://github.com/aheath1992/dnstool>

# BUGS

Report bugs at <https://github.com/aheath1992/dnstool/issues>.
