from ondewo.utils.base_client import BaseClient
from ondewo.utils.base_client_config import BaseClientConfig

from ondewo.sip.client.services.sip import Sip
from ondewo.sip.client.services_container import ServicesContainer


class Client(BaseClient):
    """
    The core python client for interacting with ONDEWO SIP services.
    """

    def _initialize_services(self, config: BaseClientConfig, use_secure_channel: bool) -> None:
        """
        Login with the current config and setup the services in self.services

        Returns:
            None
        """
        self.services: ServicesContainer = ServicesContainer(
            sip=Sip(config=config, use_secure_channel=use_secure_channel),
        )
