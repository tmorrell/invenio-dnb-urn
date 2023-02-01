# -*- coding: utf-8 -*-
#
# Copyright (C) 2022, 2023 University of Münster.
#
# Invenio-Dnb-Urn is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Helpers for serializers."""

from invenio_access.permissions import system_identity
from invenio_search.engine import dsl
from invenio_vocabularies.proxies import current_service as vocabulary_service

from .errors import VocabularyItemNotFoundError


def get_vocabulary_props(vocabulary, fields, id_):
    """Returns props associated with a vocabulary, id_."""
    # This is ok given that read_all is cached per vocabulary+fields and
    # is reused overtime
    results = vocabulary_service.read_all(
        system_identity,
        ["id"] + fields,
        vocabulary,
        extra_filter=dsl.Q("term", id=id_),
    )

    for h in results.hits:
        return h.get("props", {})

    raise VocabularyItemNotFoundError(
        f"The '{vocabulary}' vocabulary item '{id_}' was not found."
    )
