#!/usr/bin/env python3
"""
SNMP GET example using PySNMP 7.x asyncio API.

Queries a single OID and prints a human-readable result.
Written in a production-style structure so it can be reused in larger
network automation tooling.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from pysnmp.hlapi.v3arch.asyncio import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    get_cmd,
)

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class SnmpTarget:
    """Connection details for an SNMP target."""

    host: str
    port: int = 161
    community: str = "secret"
    timeout: int = 2
    retries: int = 1


@dataclass(frozen=True, slots=True)
class SnmpResult:
    """Represents a decoded SNMP GET response."""

    oid: str
    value: str


class SnmpQueryError(Exception):
    """Raised when an SNMP query fails."""


def decode_snmp_value(value: Any) -> str:
    """
    Convert a PySNMP value into a readable string.

    OctetString values may render as hex via prettyPrint(), so prefer
    decoding raw octets first. Fall back safely when needed.
    """
    if hasattr(value, "asOctets"):
        raw_value = value.asOctets()
        try:
            return raw_value.decode("utf-8")
        except UnicodeDecodeError:
            return raw_value.decode("latin-1", errors="replace")

    return value.prettyPrint()


async def snmp_get(target: SnmpTarget, oid: str) -> SnmpResult:
    """
    Perform a single SNMP GET operation.

    Args:
        target: SNMP target configuration.
        oid: OID to query.

    Returns:
        SnmpResult containing the resolved OID and decoded value.

    Raises:
        SnmpQueryError: If the SNMP engine, transport, or agent reports an error.
    """
    error_indication, error_status, error_index, var_binds = await get_cmd(
        SnmpEngine(),
        CommunityData(target.community),
        await UdpTransportTarget.create(
            (target.host, target.port),
            timeout=target.timeout,
            retries=target.retries,
        ),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
    )

    if error_indication:
        raise SnmpQueryError(f"SNMP engine/transport error: {error_indication}")

    if error_status:
        failed_oid = (
            var_binds[int(error_index) - 1][0].prettyPrint()
            if error_index and var_binds
            else "unknown"
        )
        raise SnmpQueryError(
            f"SNMP agent error: {error_status.prettyPrint()} at {failed_oid}"
        )

    if not var_binds:
        raise SnmpQueryError("SNMP response contained no variable bindings")

    returned_oid, returned_value = var_binds[0]
    return SnmpResult(
        oid=returned_oid.prettyPrint(),
        value=decode_snmp_value(returned_value),
    )


async def main() -> int:
    """
    Program entry point.

    Returns:
        Process exit code.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    target = SnmpTarget(
        host="10.10.10.101",
        port=161,
        community="secret",
        timeout=2,
        retries=1,
    )
    oid = "1.3.6.1.4.1.9.2.1.61.0"

    try:
        result = await snmp_get(target=target, oid=oid)
    except SnmpQueryError as exc:
        LOGGER.error("%s", exc)
        return 1

    print(f"{result.oid} = {result.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
