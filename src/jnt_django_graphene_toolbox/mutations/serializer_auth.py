from typing import Optional

from graphene.types.mutation import MutationOptions
from graphql import ResolveInfo

from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied
from jnt_django_graphene_toolbox.mutations import SerializerMutation


class SerializerAuthMutationOptions(MutationOptions):
    """Serializer auth mutation options."""

    permission_classes = None


class SerializerAuthMutation(SerializerMutation):
    """Serializer mutation with authorization support."""

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(  # noqa: WPS211
        cls,
        permission_classes=None,
        _meta=None,
        **options,
    ):
        """Initialize class with meta."""
        if not _meta:
            _meta = SerializerAuthMutationOptions(cls)  # noqa: WPS122

        _meta.permission_classes = permission_classes
        super().__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def internal_mutate(
        cls, root, info, **kwargs,  # noqa: WPS110
    ) -> "SerializerMutation":
        """Overrided mutate handler with permissions check."""
        cls.check_premissions(root, info, **kwargs)
        return super().internal_mutate(root, info, **kwargs)

    @classmethod
    def check_premissions(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **input,  # noqa: WPS125
    ) -> None:
        """Check permissions."""
        has_permission = all(
            perm().has_mutation_permission(root, info, **input)
            for perm in cls._meta.permission_classes
        )

        if not has_permission:
            raise GraphQLPermissionDenied
