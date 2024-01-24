from abc import ABC, abstractmethod

from src.common import api


class OtaUpdate(ABC):
    """Class used to check if over-the-air update (OTA) is needed."""
    _update_check: str
    _pull_firmware_url: str

    def __init__(self, update_check: str, pull_firmware_url: str):
        """
        Parameters
        ----------
        update_check : str
            Url to check if update is needed. Url has to be a GET request.
        pull_firmware_url : str
            Url used to fetch new changes. Url has to be a GET request.
        """
        self._update_check = update_check
        self._pull_firmware_url = pull_firmware_url

    @abstractmethod
    def _check_url(self, version: str):
        """Method used to create full request url based on request url."""
        pass

    @abstractmethod
    def _check_response(self, response: {}) -> [bool, str]:
        """Method used to validate if update is needed."""
        pass

    @abstractmethod
    def _update_needed(self, current_version: str, next_version: str) -> bool:
        """Method used to validate if current version is older than next."""
        pass

    @abstractmethod
    def _update_url(self, version: str):
        """Method used to create full request url based on request url."""
        pass

    @abstractmethod
    def _update_response(self, response) -> bool:
        """Method used to validate if update is needed."""
        pass

    @abstractmethod
    def _update_process(self, response) -> bool:
        """Method used to process with update."""
        pass

    def check(self, version: str) -> bool:
        """
        Check if update is needed.

        Parameters
        ----------
        version : str
            Current/last version that is installed on the device.

        Returns
        -------
        bool
            If update is needed, or not.
        """
        url = self._check_url(version=version)
        response = api.get(url)
        if not response:
            return False
        needed, new_version = self._check_response(response=response)
        if not needed:
            return False
        return self._update_needed(current_version=version, next_version=new_version)

    def update(self, version: str) -> bool:
        """
        Update device to next version.

        Parameters
        ----------
        version : str
            Current/last version that is installed on the device.
        """
        url = self._update_url(version=version)
        response = api.get(url)
        if not response:
            return False
        data = self._update_response(response=response)
        if not data:
            return False
        return self._update_process(response=data)
