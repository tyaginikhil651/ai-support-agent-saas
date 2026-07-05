from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

from auth.routes import router as auth_router
from auth.dependencies import get_current_admin, require_roles
from auth.auth_service import login_and_get_token
from tenant_operations import (
    get_tenant_sessions,
    get_tenant_escalated_tickets,
    get_tenant_vip_customers,
    get_tenant_customer_profile,
    get_tenant_analytics
)

from tenant_queries import (
    get_dashboard_metrics,
    get_tenant_customers,
    get_tenant_tickets,
    get_tenant_appointments,
    get_tenant_ticket_by_id,
    update_tenant_ticket_status
)
from tenant_reply_service import (
    get_tenant_ticket_for_reply,
    get_tenant_customer_by_platform_id,
    save_tenant_reply,
    get_tenant_replies,
    mark_tenant_ticket_in_progress
)

from services.tenant_whatsapp_service import (
    get_tenant_by_phone_number_id
)

from database import get_connection
from whatsapp_service import send_whatsapp_message
from live.manager import manager
from auth.websocket_auth import get_websocket_admin
from fastapi import WebSocket, WebSocketDisconnect
from config import APP_SECRET_KEY
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI(
    title="AI Support Agent Dashboard"
)

app.include_router(auth_router)


# ----------------------------------
# TEMPLATES
# ----------------------------------

templates = Jinja2Templates(
    directory="templates"
)


# ----------------------------------
# STATIC FILES
# ----------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)




app.add_middleware(
    SessionMiddleware,
    secret_key=APP_SECRET_KEY,
    https_only=False,
    same_site="lax"
)

# ----------------------------------
# BROWSER AUTH ERROR HANDLER
# Redirect unauthenticated dashboard users to login.
# ----------------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    protected_browser_routes = [
        "/",
        "/customers",
        "/tickets",
        "/appointments"
    ]

    is_ticket_page = request.url.path.startswith("/ticket/")

    if (
        exc.status_code == 401
        and (
            request.url.path in protected_browser_routes
            or is_ticket_page
        )
    ):
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        }
    )


# ----------------------------------
# LOGIN
# ----------------------------------

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": None
        }
    )


@app.post("/login")
def login_submit(
    request: Request,
    tenant_slug: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    result = login_and_get_token(
        tenant_slug=tenant_slug,
        username=username,
        password=password
    )

    if not result:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Invalid company slug, username, or password"
            },
            status_code=401
        )

    response = RedirectResponse(
        url="/",
        status_code=303
    )

    # Development only: secure=False works on localhost.
    # Change to secure=True after HTTPS is enabled in production.
    response.set_cookie(
        key="access_token",
        value=result["token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24
    )

    return response


@app.get("/logout")
def logout():
    response = RedirectResponse(
        url="/login",
        status_code=303
    )

    response.delete_cookie(
        key="access_token"
    )

    return response


# ----------------------------------
# DASHBOARD
# ----------------------------------

@app.get("/")
def dashboard(
    request: Request,
    admin=Depends(get_current_admin)
):
    tenant_id = admin["tenant_id"]

    metrics = get_dashboard_metrics(tenant_id)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "admin": admin,
            "customers": metrics["customers"],
            "tickets": metrics["open_tickets"],
            "appointments": metrics["appointments"],
            "live_tickets": metrics["live_tickets"],
            "high_priority": metrics["high_priority"]
        }
    )


# ----------------------------------
# CUSTOMERS
# ----------------------------------

@app.get("/customers")
def customers(
    request: Request,
    admin=Depends(get_current_admin)
):
    users = get_tenant_customers(
        admin["tenant_id"]
    )

    return templates.TemplateResponse(
        request=request,
        name="customers.html",
        context={
            "admin": admin,
            "users": users
        }
    )


# ----------------------------------
# TICKETS
# ----------------------------------

@app.get("/tickets")
def tickets(
    request: Request,
    admin=Depends(get_current_admin)
):
    ticket_rows = get_tenant_tickets(
        admin["tenant_id"]
    )

    return templates.TemplateResponse(
        request=request,
        name="tickets.html",
        context={
            "admin": admin,
            "tickets": ticket_rows
        }
    )


# ----------------------------------
# APPOINTMENTS
# ----------------------------------

@app.get("/appointments")
def appointments(
    request: Request,
    admin=Depends(get_current_admin)
):
    appointment_rows = get_tenant_appointments(
        admin["tenant_id"]
    )

    return templates.TemplateResponse(
        request=request,
        name="appointments.html",
        context={
            "admin": admin,
            "appointments": appointment_rows
        }
    )


# ----------------------------------
# TICKET DETAILS
# ----------------------------------

# @app.get("/ticket/{ticket_id}")
# def ticket_details(
#     request: Request,
#     ticket_id: str,
#     admin=Depends(get_current_admin)
# ):
#     ticket = get_tenant_ticket_by_id(
#         admin["tenant_id"],
#         ticket_id
#     )

#     if not ticket:
#         raise HTTPException(
#             status_code=404,
#             detail="Ticket not found for this company"
#         )

#     return templates.TemplateResponse(
#         request=request,
#         name="ticket_detail.html",
#         context={
#             "admin": admin,
#             "ticket": ticket
#         }
#     )

@app.get("/ticket/{ticket_id}")
def ticket_details(
    request: Request,
    ticket_id: str,
    admin=Depends(get_current_admin)
):
    tenant_id = admin["tenant_id"]

    ticket = get_tenant_ticket_by_id(
        tenant_id,
        ticket_id
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found for this company"
        )

    replies = get_tenant_replies(
        tenant_id,
        ticket_id
    )

    return templates.TemplateResponse(
        request=request,
        name="ticket_detail.html",
        context={
            "admin": admin,
            "ticket": ticket,
            "replies": replies
        }
    )

# ----------------------------------
# TICKET STATUS UPDATE
# Owner, manager, and agent can update tickets.
# ----------------------------------

@app.post("/ticket/update")
def update_ticket(
    ticket_id: str = Form(...),
    status: str = Form(...),
    admin=Depends(
        require_roles(
            "owner",
            "manager",
            "agent"
        )
    )
):
    updated = update_tenant_ticket_status(
        admin["tenant_id"],
        ticket_id,
        status
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found for this company"
        )

    return {
        "success": True,
        "message": "Ticket updated successfully"
    }


@app.post("/reply")
def reply_to_customer(
    ticket_id: str = Form(...),
    message: str = Form(...),
    admin=Depends(
        require_roles(
            "owner",
            "manager",
            "agent"
        )
    )
):
    tenant_id = admin["tenant_id"]

    clean_ticket_id = ticket_id.strip().upper()
    clean_message = message.strip()

    if not clean_message:
        raise HTTPException(
            status_code=400,
            detail="Reply message cannot be empty"
        )

    ticket = get_tenant_ticket_for_reply(
        tenant_id,
        clean_ticket_id
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found for this company"
        )

    customer = get_tenant_customer_by_platform_id(
        tenant_id,
        ticket["user_id"]
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found for this ticket"
        )

    sender_name = admin.get("username", "Support Agent")

    # Save reply first, even if WhatsApp delivery later fails.
    save_tenant_reply(
        tenant_id=tenant_id,
        ticket_id=clean_ticket_id,
        message=clean_message,
        sender=sender_name
    )

    mark_tenant_ticket_in_progress(
        tenant_id=tenant_id,
        ticket_id=clean_ticket_id
    )

    whatsapp_sent = False
    whatsapp_error = None

    try:
        conn = get_connection()

        whatsapp_config = conn.execute(
            """
            SELECT phone_number_id
            FROM tenant_whatsapp_numbers
            WHERE tenant_id = ?
            AND active = 1
            LIMIT 1
            """,
            (tenant_id,)
        ).fetchone()

        conn.close()

        if whatsapp_config and customer["phone"]:
            send_whatsapp_message(
                to=customer["phone"],
                text=clean_message,
                phone_number_id=whatsapp_config["phone_number_id"]
            )

            whatsapp_sent = True

        elif not whatsapp_config:
            whatsapp_error = "No active WhatsApp number configured for this company"

        elif not customer["phone"]:
            whatsapp_error = "Customer does not have a phone number"

    except Exception as e:
        whatsapp_error = str(e)
        print("WhatsApp reply delivery error:", whatsapp_error)

    return {
        "success": True,
        "ticket_id": clean_ticket_id,
        "message": "Reply saved successfully",
        "whatsapp_sent": whatsapp_sent,
        "whatsapp_error": whatsapp_error
    }


@app.get("/sessions")
def sessions_page(
    request: Request,
    admin=Depends(
        require_roles(
            "owner",
            "manager",
            "agent"
        )
    )
):
    sessions = get_tenant_sessions(
        admin["tenant_id"]
    )

    return templates.TemplateResponse(
        request=request,
        name="sessions.html",
        context={
            "admin": admin,
            "sessions": sessions
        }
    )



@app.get("/escalated")
def escalated(
    request: Request,
    admin=Depends(
        require_roles(
            "owner",
            "manager",
            "agent"
        )
    )
):
    tickets = get_tenant_escalated_tickets(
        admin["tenant_id"]
    )

    return templates.TemplateResponse(
        request=request,
        name="escalated.html",
        context={
            "admin": admin,
            "tickets": tickets
        }
    )

@app.get("/vip-customers")
def vip_customers(
    request: Request,
    admin=Depends(
        require_roles(
            "owner",
            "manager"
        )
    )
):
    users = get_tenant_vip_customers(
        admin["tenant_id"]
    )

    return templates.TemplateResponse(
        request=request,
        name="vip_customers.html",
        context={
            "admin": admin,
            "users": users
        }
    )


@app.get("/profile/{user_id}")
def profile(
    user_id: str,
    admin=Depends(
        require_roles(
            "owner",
            "manager",
            "agent"
        )
    )
):
    user = get_tenant_customer_profile(
        tenant_id=admin["tenant_id"],
        user_id=user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Customer profile not found for this company"
        )

    return {
        "user": dict(user)
    }

@app.get("/analytics")
def analytics_page(
    request: Request,
    admin=Depends(
        require_roles(
            "owner",
            "manager"
        )
    )
):
    analytics_data = get_tenant_analytics(
        admin["tenant_id"]
    )

    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "admin": admin,
            **analytics_data
        }
    )


# ----------------------------------
# HEALTH CHECK
# ----------------------------------

@app.get("/health")
def health():
    return {
        "status": "running"
    }


@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    admin = await get_websocket_admin(websocket)

    if not admin:
        return

    tenant_id = admin["tenant_id"]

    await manager.connect(
        tenant_id=tenant_id,
        websocket=websocket
    )

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(
            tenant_id=tenant_id,
            websocket=websocket
        )

# ----------------------------------
# RUN DIRECTLY
# ----------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "admin_dashboard:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
