from services.tenant_service import (
    create_company
)

from auth.auth_service import (
    create_owner
)


def signup_company(

    company_name,

    owner_name,

    email,

    password,

    phone
):

    company = create_company(

        company_name,

        email,

        phone
    )

    create_owner(

        company["id"],

        owner_name,

        email,

        password
    )

    return company