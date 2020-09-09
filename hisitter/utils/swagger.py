""" Swagger utils module has the additional swagger configurations."""

# Swagger
from drf_yasg.openapi import Parameter

is_authenticated_permission = Parameter(
    name='Is Authenticated Permission',
    in_='header',
    description="""
    You need to have an account and access token, that will be send in the next
    format:
    KEY             VALUE
    Authorization   Token <token>
    """,
    required=True,
    type='string'
)

is_client_permission = Parameter(
    name='Is Client permission',
    in_='header',
    description="""
    You need to have an account, access token further you
    need to be client user to access in this view.
    The access token must be send, in the next
    format:
    KEY             VALUE
    Authorization   Token <token>
    """,
    required=True,
    type='string'
)

is_account_owner_permission = Parameter(
    name='Is Account owner permission',
    in_='header',
    description="""
    This view is a detail, for that you need to be the 
    account owner of the detail, if you want access.
    The access token must be send, in the next
    format:
    KEY             VALUE
    Authorization   Token <token>
    """,
    required=True,
    type='string'
)

is_service_owner_permission = Parameter(
    name='Is Service owner permission',
    in_='header',
    description="""
    This permission is to verify if the client is owner of the
    service, because only the client can give a review, the
    access token is the mechanism to validate that.
    The access token must be send, in the next
    format:
    KEY             VALUE
    Authorization   Token <token>
    """,
    required=True,
    type='string'
)
