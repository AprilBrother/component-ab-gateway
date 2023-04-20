import logging
from typing import (
    Iterable,
    Union,
    Dict,
    List
)
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from .const import (
    INDEX_ADV,
    INDEX_MAC,
    INDEX_RSSI
)

_LOGGER = logging.getLogger(__name__)
_HISTORY = {}

def _long_uuid(uuid: str) -> str:
    """Convert a UUID to a long UUID."""
    return (
        f"0000{uuid.lower()}-0000-1000-8000-00805f9b34fb" if len(uuid) < 8 else uuid
    ).lower()

def _convert_address(s: str) -> str:
    """Convert an string to an mac address."""
    return ':'.join(s[i:i+2] for i in range(0, len(s), 2))

def parse_data(dev):
    """Parse the raw data."""

    data = dev[INDEX_ADV]
    rssi = dev[INDEX_RSSI]
    adpayload_start = 0
    try:
        adpayload_size = len(data) - adpayload_start
    except IndexError:
        return None

    complete_local_name = ""
    shortened_local_name = ""
    service_class_uuid16 = None
    service_class_uuid128 = None
    service_data_list = []
    man_spec_data_list = []

    while adpayload_size > 1:
        adstuct_size = data[adpayload_start] + 1
        if adstuct_size > 1 and adstuct_size <= adpayload_size:
            adstruct = data[adpayload_start:adpayload_start + adstuct_size]
            # https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile/
            adstuct_type = adstruct[1]
            if adstuct_type == 0x02:
                # AD type 'Incomplete List of 16-bit Service Class UUIDs'
                service_class_uuid16 = adstruct[2:4]
            elif adstuct_type == 0x03:
                # AD type 'Complete List of 16-bit Service Class UUIDs'
                service_class_uuid16 = adstruct[2:4]
            elif adstuct_type == 0x06:
                # AD type '128-bit Service Class UUIDs'
                service_class_uuid128 = adstruct[2:]
            elif adstuct_type == 0x08:
                # AD type 'shortened local name'
                shortened_local_name = adstruct[2:].decode("utf-8")
            elif adstuct_type == 0x09:
                # AD type 'complete local name'
                complete_local_name = adstruct[2:].decode("utf-8")
            elif adstuct_type == 0x16 and adstuct_size > 4:
                # AD type 'Service Data - 16-bit UUID'
                service_data_list.append(adstruct)
            elif adstuct_type == 0xFF:
                # AD type 'Manufacturer Specific Data'
                man_spec_data_list.append(adstruct)
                # https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers/

        adpayload_size -= adstuct_size
        adpayload_start += adstuct_size

    address = _convert_address(dev[INDEX_MAC])
    name = shortened_local_name if complete_local_name == "" else complete_local_name
    if name == "":
        if _HISTORY.get(address):
            name = _HISTORY.get(address)
    else:
        _HISTORY[address] = name

    manufacturer_data = {}
    if (len(man_spec_data_list)):
        man = man_spec_data_list[0]
        manufacturer_id = int.from_bytes(man[2:4], byteorder="little")
        manufacturer_value = man[4:]
        manufacturer_data[manufacturer_id] = manufacturer_value

    service_uuids = []
    if (service_class_uuid16):
        service_uuids.append(_long_uuid(service_class_uuid16[::-1].hex()))
    if (service_class_uuid128):
        service_uuids.append(service_class_uuid128.hex())

    service_data = {}
    if (len(service_data_list)):
        svc = service_data_list[0]
        service_uuid = _long_uuid(svc[2:4][::-1].hex())
        service_data[service_uuid] = svc[4:]

    advertisement_data = AdvertisementData(
        local_name=None if name == "" else name,
        manufacturer_data=manufacturer_data,
        service_data=service_data,
        service_uuids=service_uuids,
        tx_power=-127,
        rssi=rssi,
        platform_data=(),
    )

    device = BLEDevice(  # type: ignore[no-untyped-call]
        address=address,
        name=name,
        details=None,
        rssi=rssi,  # deprecated, will be removed in newer bleak
    )
    _LOGGER.debug("parsed adv: %s device: %s service_uuids: %s", advertisement_data, device, advertisement_data.service_uuids)
    return device, advertisement_data


