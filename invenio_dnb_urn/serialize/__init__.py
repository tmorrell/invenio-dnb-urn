# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 University of Münster.
#
# Invenio-Dnb-Urn is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from .epicur import InvenioSerializerEpicur
from.xmetadiss import InvenioSerializerXMetaDissPlus

__all__ = (
    "InvenioSerializerEpicur",
    "InvenioSerializerXMetaDissPlus",
)
