# from swarms.telemetry.main import Telemetry  # noqa: E402, F403
from swarms.telemetry.bootup import bootup  # noqa: E402, F403
from swarms.telemetry.user_utils import (
    get_user_device_data,
)  # noqa: E402, F403

bootup()

get_user_device_data()

from swarms.agents import *  # noqa: E402, F403
from swarms.structs import *  # noqa: E402, F403
from swarms.models import *  # noqa: E402, F403
from swarms.telemetry import *  # noqa: E402, F403
from swarms.utils import *  # noqa: E402, F403
from swarms.prompts import *  # noqa: E402, F403
from swarms.tokenizers import *  # noqa: E402, F403
from swarms.loaders import *  # noqa: E402, F403
from swarms.artifacts import *  # noqa: E402, F403
from swarms.chunkers import *  # noqa: E402, F403
