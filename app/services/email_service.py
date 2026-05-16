from flask_mail import Message
from flask import render_template, url_for
from app.extensions.db import mail
import threading


def _send_async(msg):
    try:
        with mail.connect() as conn:
            conn.send(msg)

        print(f"Email sent to {msg.recipients}")

    except Exception as e:
        print(f"MAIL ERROR: {e}")


def send_welcome_email(to_email, name):
    msg = Message(
        subject="Welcome to CampusXHire 🎓",
        recipients=[to_email]
    )

    msg.html = render_template(
        "email/welcome.html",
        name=name
    )

    threading.Thread(
        target=_send_async,
        args=(msg,),
        daemon=True
    ).start()


def send_otp_email(email, otp):
    msg = Message(
        subject="CampusXHire OTP Verification",
        recipients=[email]
    )

    msg.html = render_template(
        "email/otp.html",
        otp=otp
    )

    threading.Thread(
        target=_send_async,
        args=(msg,),
        daemon=True
    ).start()


def send_job_mail(student, job):
    msg = Message(
        subject=f"Job Application Received: {job.job_title}",
        recipients=[student.email]
    )

    apply_link = url_for(
        "student.job_details",
        job_id=job.id,
        _external=True
    )

    msg.html = render_template(
        "student/job_match.html",
        student=student,
        job=job,
        apply_link=apply_link
    )

    threading.Thread(
        target=_send_async,
        args=(msg,),
        daemon=True
    ).start()


def send_approval_email(
    student_email,
    student_name,
    job_title,
    company_name,
    status
):
    msg = Message(
        subject=f"Application {status}: {job_title}",
        recipients=[student_email]
    )

    template_name = (
        "email/application_approved.html"
        if str(status).lower() == "approved"
        else "email/application_status.html"
    )

    msg.html = render_template(
        template_name,
        student_name=student_name,
        job_title=job_title,
        company_name=company_name,
        status=status
    )

    threading.Thread(
        target=_send_async,
        args=(msg,),
        daemon=True
    ).start()
