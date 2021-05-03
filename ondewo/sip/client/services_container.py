from dataclasses import dataclass

from ondewo.utils.base_service_container import BaseServicesContainer

from ondewo.sip.client.services.sip import Sip


@dataclass
class ServicesContainer(BaseServicesContainer):
    sip: Sip
