import asyncio
import datetime
from pysnmp.hlapi.v3arch.asyncio import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    get_cmd,
)

system_name = "1.3.6.1.2.1.1.5.0"
gig0_0_in_oct = "1.3.6.1.2.1.2.2.1.10.1"
gig0_0_in_uPackets = "1.3.6.1.2.1.2.2.1.11.1"
gig0_0_out_oct = "1.3.6.1.2.1.2.2.1.16.1"
gig0_0_out_uPackets = "1.3.6.1.2.1.2.2.1.17.1"

host = "10.10.10.101"
community = "secret"


async def snmp_get(host, community, oid):
    _, _, _, var_binds = await get_cmd(
        SnmpEngine(),
        CommunityData(community),
        await UdpTransportTarget.create((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
    )

    for _, value in var_binds:
        if hasattr(value, "asOctets"):
            return value.asOctets().decode("utf-8")
        return value.prettyPrint()


async def main():
    result = {}
    result["Time"] = datetime.datetime.now().astimezone().isoformat()
    result["hostname"] = await snmp_get(host, community, system_name)
    result["Gig0-0_In_Octet"] = await snmp_get(host, community, gig0_0_in_oct)
    result["Gig0-0_In_uPackets"] = await snmp_get(host, community, gig0_0_in_uPackets)
    result["Gig0-0_Out_Octet"] = await snmp_get(host, community, gig0_0_out_oct)
    result["Gig0-0_Out_uPackets"] = await snmp_get(host, community, gig0_0_out_uPackets)

    with open("/home/cliffdev/Mastering-Python-Networking-Fourth-Edition/Chapter07/results.txt", "a") as f:
        f.write(f"{result}\n")

    print(result)


if __name__ == "__main__":
    asyncio.run(main())