version = "1.0.0"

"""
Status of instances
"""
INSTANCE_STATUS_UP: str = "UP"
INSTANCE_STATUS_DOWN: str = "DOWN"
INSTANCE_STATUS_STARTING: str = "STARTING"
INSTANCE_STATUS_OUT_OF_SERVICE: str = "OUT_OF_SERVICE"
INSTANCE_STATUS_UNKNOWN: str = "UNKNOWN"

"""
Action type of instances
"""
ACTION_TYPE_ADDED: str = "ADDED"
ACTION_TYPE_MODIFIED: str = "MODIFIED"
ACTION_TYPE_DELETED: str = "DELETED"

"""
This is for the DiscoveryClient, when this strategy is set, get_service_url will random choose one of the UP instance 
and return its url. This is the default strategy
"""
HA_STRATEGY_RANDOM: int = 1
"""
This is for the DiscoveryClient, when this strategy is set, get_service_url will always return one instance until it is
down.
"""
HA_STRATEGY_STICK: int = 2
"""
This is for the DiscoveryClient, when this strategy is set, get_service_url will always return a new instance if 
any other instances are up.
"""
HA_STRATEGY_OTHER: int = 3

"""
The error types that will send back to on_error callback function
"""
ERROR_REGISTER: str = "EUREKA_ERROR_REGISTER"
ERROR_DISCOVER: str = "EUREKA_ERROR_DISCOVER"
ERROR_STATUS_UPDATE: str = "EUREKA_ERROR_STATUS_UPDATE"

"""
Default eureka server url.
"""
DEFAULT_EUREKA_SERVER_URL = "http://127.0.0.1:8761/"

"""
Default instance field values
"""
DEFAULT_INSTANCE_PORT = 9090
DEFAULT_INSTANCE_SECURE_PORT = 9443
RENEWAL_INTERVAL_IN_SECS = 30
DURATION_IN_SECS = 90
DEFAULT_DATA_CENTER_INFO = "MyOwn"
DEFAULT_DATA_CENTER_INFO_CLASS = (
    "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo"
)
AMAZON_DATA_CENTER_INFO_CLASS = "com.netflix.appinfo.AmazonInfo"

"""
Default configurations
"""
DEFAULT_ENCODING = "utf-8"
DEFAULT_ZONE = "fa-ir"

"""
The timeout seconds that all http request to the eureka server
"""
DEFAULT_TIME_OUT = 5
