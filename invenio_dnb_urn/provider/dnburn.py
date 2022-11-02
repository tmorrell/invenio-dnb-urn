# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 University of Münster.
#
# Invenio-Dnb-Urn is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import warnings

from dnb_urn_service import DNBUrnServiceRESTClient
from flask import current_app
from invenio_pidstore.models import PIDStatus
from invenio_rdm_records.services.pids.providers import PIDProvider


class DNBUrnClient:
    """DNB Urn Client."""

    def __init__(self, name, config_prefix=None, **kwargs):
        """Constructor."""
        self.name = name
        self._config_prefix = config_prefix or "URN_DNB"
        self._api = None

    def cfgkey(self, key):
        """Generate a configuration key."""
        return f"{self._config_prefix}_{key.upper()}"

    def cfg(self, key, default=None):
        """Get a application config value."""
        return current_app.config.get(self.cfgkey(key), default)

    def generate_urn(self, record):
        """Generate a URN."""
        self.check_credentials()
        prefix = self.cfg("id_prefix")
        if not prefix:
            raise RuntimeError("Invalid URN prefix configured.")
        urn_format = self.cfg("format", "{prefix}-{id}")
        return urn_format.format(prefix=prefix, id=record.pid.pid_value)

    def check_credentials(self, **kwargs):
        """Returns if the client has the credentials properly set up.
        If the client is running on test mode the credentials are required, too.
        """
        if not (self.cfg("username") and self.cfg("password") and self.cfg("id_prefix")):
            warnings.warn(
                f"The {self.__class__.__name__} is misconfigured. Please "
                f"set {self.cfgkey('username')}, {self.cfgkey('password')}"
                f" and {self.cfgkey('id_prefix')} in your configuration.",
                UserWarning,
            )

    @property
    def api(self):
        """DNB URN Service API client instance."""
        if self._api is None:
            self.check_credentials()
            self._api = DNBUrnServiceRESTClient(
                self.cfg("username"),
                self.cfg("password"),
                self.cfg("id_prefix"),
                self.cfg("test_mode", True),
            )
        return self._api


class DnbUrnProvider(PIDProvider):
    """URN provider."""

    name = "urn"

    def __init__(
        self,
        name,
        client=None,
        **kwargs):
        """Constructor."""
        super().__init__(
            name,
            pid_type="urn",
            default_status=PIDStatus.NEW,
            managed=True,
            **kwargs,
        )

    def generate_id(self, record, **kwargs):
        """Generates an identifier value."""
        prefix = current_app.config.get("URN_DNB_ID_PREFIX", "")
        return f"urn:nbn:{prefix}{record.pid.pid_value}"

    def reserve(self, pid, record, **kwargs):
        """Constant True.

        PID default status is registered.
        NBN registration is passive by harvesting OAI with metadataPrefix=epicur.
        """
        return True
