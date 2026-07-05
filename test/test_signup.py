from services.signup_service import (
    signup_company
)

company = signup_company(

    "ABC Internet",

    "nikhil",

    "admin@abc.com",

    "123456",

    "+919999999999"
)

print(company)