import hashlib
import platform
import uuid
import socket
from swarms.telemetry.sys_info import system_info
from swarms.telemetry.check_update import check_for_package


# Helper functions
def generate_user_id():
    """Generate user id

    Returns:
        _type_: _description_
    """
    return str(uuid.uuid4())


def get_machine_id():
    """Get machine id

    Returns:
        _type_: _description_
    """
    raw_id = platform.node()
    hashed_id = hashlib.sha256(raw_id.encode()).hexdigest()
    return hashed_id


def get_system_info():
    """
    Gathers basic system information.

    Returns:
        dict: A dictionary containing system-related information.
    """
    info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "mac_address": ":".join(
            [
                "{:02x}".format((uuid.getnode() >> elements) & 0xFF)
                for elements in range(0, 2 * 6, 8)
            ][::-1]
        ),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "Misc": system_info(),
    }
    return info


def generate_unique_identifier():
    """Generate unique identifier

    Returns:
        str: unique id

    """
    system_info = get_system_info()
    unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, str(system_info))
    return str(unique_id)


def get_local_ip():
    """Get local ip

    Returns:
        str: local ip

    """
    return socket.gethostbyname(socket.gethostname())


def get_user_device_data():
    data = {
        "ID": generate_user_id(),
        "Machine ID": get_machine_id(),
        "System Info": get_system_info(),
        "UniqueID": generate_unique_identifier(),
        "Swarms [Version]": check_for_package("swarms"),
    }
    return data


#
