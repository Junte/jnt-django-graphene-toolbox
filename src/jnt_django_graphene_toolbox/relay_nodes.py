# -*- coding: utf-8 -*-

from graphene import relay
from graphql import ResolveInfo

from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied
from jnt_django_graphene_toolbox.security.permissions import (
    AllowAny,
    AllowAuthenticated,
)


class DatasourceRelayNode(relay.Node):
    """Datasource relay node."""

    permission_classes = (AllowAuthenticated,)

    @classmethod
    def get_node_from_global_id(
        cls, info, global_id, only_type=None,  # noqa: WPS110
    ):
        """Get node by global id."""
        if cls._is_invalid_node(global_id, only_type):
            return None

        if not cls.has_permission(info, global_id):
            raise GraphQLPermissionDenied()

        get_node = getattr(only_type, "get_node", None)
        if get_node:
            return get_node(info, global_id)

    @classmethod
    def from_global_id(cls, global_id: int) -> int:
        """Returns the type name and ID used to create it."""
        return global_id

    @classmethod
    def to_global_id(cls, obj_type: str, obj_id: int) -> int:
        """Takes a type name and an ID, returns a "global ID"."""
        return obj_id

    @classmethod
    def has_permission(
        cls, info: ResolveInfo, obj_id: str,  # noqa: WPS110
    ) -> bool:
        """Check if user has permissions."""
        return all(
            perm().has_node_permission(info, obj_id)
            for perm in cls.permission_classes
        )

    @classmethod
    def _is_invalid_node(cls, global_id, only_type=None) -> bool:
        return (
            not global_id
            or not only_type
            # We make sure the ObjectType implements the "Node" interface
            or cls not in only_type._meta.interfaces  # noqa: WPS437
        )


class DatasourceRelayNodeAllowAny(DatasourceRelayNode):
    """Datasource relay node which doesn't check authentication."""

    permission_classes = (AllowAny,)