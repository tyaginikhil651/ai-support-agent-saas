from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request

from database import get_connection

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def dashboard(request: Request):

    conn = get_connection()

    users = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    appointments = conn.execute(
        "SELECT COUNT(*) FROM appointments"
    ).fetchone()[0]

    complaints = conn.execute(
        "SELECT COUNT(*) FROM complaints"
    ).fetchone()[0]

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "users": users,
            "appointments": appointments,
            "complaints": complaints
        }
    )

@app.get("/users")
def users_page(request: Request):

    conn = get_connection()

    users = conn.execute(
        "SELECT * FROM users"
    ).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={
            "users": users
        }
    )

@app.get("/appointments")
def appointments_page(request: Request):

    conn = get_connection()

    appointments = conn.execute(
        """
        SELECT *
        FROM appointments
        """
    ).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="appointments.html",
        context={
            "appointments": appointments
        }
    )

@app.get("/complaints")
def complaints_page(request: Request):

    conn = get_connection()

    complaints = conn.execute(
        "SELECT * FROM complaints"
    ).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="complaints.html",
        context={
            "complaints": complaints
        }
    )

@app.post("/close-ticket/{ticket_id}")
def close_ticket(ticket_id: str):

    conn = get_connection()

    conn.execute(
        """
        UPDATE complaints
        SET status='closed'
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    conn.commit()
    conn.close()

    return {"message": "closed"}

