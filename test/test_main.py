import pytest
import dns.resolver
from unittest.mock import MagicMock
from main import is_ip, resolve, reverse_resolve, main

@pytest.fixture(autouse=True)
def stub_resolv_conf(mocker):
    # dns.resolver.Resolver() parses /etc/resolv.conf in its constructor and
    # raises NoResolverConfiguration if no nameserver is listed. RPM build
    # chroots and CI containers often have no resolver configured, so stub the
    # read out; every test mocks Resolver.resolve anyway.
    mocker.patch("dns.resolver.Resolver.read_resolv_conf")

def test_is_ip_valid():
    assert is_ip("1.1.1.1") is True
    assert is_ip("2001:db8::1") is True

def test_is_ip_invalid():
    assert is_ip("example.com") is False
    assert is_ip("999.999.999.999") is False

def test_resolve_sucess(mocker, capsys):
    mock_resolve = mocker.patch("dns.resolver.Resolver.resolve")
    mock_a_rdata = MagicMock()
    mock_a_rdata.to_text.return_value = "192.0.2.1"

    def side_effect(qname, rdtype):
        if rdtype == "A":
            return [mock_a_rdata]
        raise dns.resolver.NoAnswer()

    mock_resolve.side_effect = side_effect

    resolve("example.com", label="test-env")
    captured = capsys.readouterr()
    assert "Hostname example.com (test-env) has the following records" in captured.out
    assert "A:\n  192.0.2.1" in captured.out

def test_resolve_nxdomain(mocker):
    mock_resolve = mocker.patch("dns.resolver.Resolver.resolve")
    mock_resolve.side_effect = dns.resolver.NXDOMAIN()

    result = resolve("nonexistent.com")
    assert result == "[-] Hostname nonexistent.com does not exist"

def test_reverse_resolve_nxdomain(mocker, capsys):
    mock_resolve = mocker.patch("dns.resolver.Resolver.resolve")
    mock_resolve.side_effect = dns.resolver.NXDOMAIN()   

    reverse_resolve("1.1.1.1")

    captured = capsys.readouterr()
    assert "[-] No PTR record found for 1.1.1.1" in captured.out

def test_main_with_hostname(mocker):
    mocker.patch("argparse.ArgumentParser.parse_args", 
        return_value=MagicMock(hostname="example.com", nameserver="8.8.8.8"))

    mock_resolve = mocker.patch("main.resolve")

    main()

    mock_resolve.assert_any_call(hostname="example.com", label="internal")
    mock_resolve.assert_any_call(hostname="example.com", 
        label="external", nameserver="8.8.8.8")

def test_main_with_ip(mocker):
    mocker.patch("argparse.ArgumentParser.parse_args",
        return_value=MagicMock(hostname="1.1.1.1", nameserver="8.8.8.8"))

    mock_reverse = mocker.patch("main.reverse_resolve")

    main()

    mock_reverse.assert_any_call(ip="1.1.1.1", label="internal")
    mock_reverse.assert_any_call(ip="1.1.1.1",
        label="external", nameserver="8.8.8.8")
