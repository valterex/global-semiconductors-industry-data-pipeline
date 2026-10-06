"""Stubs of dbt_utils macros for sqlfluff's jinja templater.

sqlfluff only needs the templated SQL to be syntactically valid so it can be
parsed and linted offline (no live warehouse). The real macro logic is provided
by dbt at build time; these stubs just return a valid SQL placeholder.
"""


def generate_surrogate_key(field_list):
    return "'surrogate_key'"
