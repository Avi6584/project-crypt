from fastapi import APIRouter, HTTPException, status
from core.dependencies import db_dependency
from models.mailModel import Mail
from schemas.mailSchema import MailSchema
from service import MailService
from email.message import EmailMessage
import smtplib
from utils.encryptDecrypt import hashPassword

router = APIRouter(
    tags=["Mail"]
)

#mail service config
mail_service = MailService(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username="testavinash216@gmail.com",
    password="hxmu ncjz rftj latv"
)

@router.post("/saveMail")
async def registerMail(req: MailSchema, db:db_dependency):
    try:

        hashedpasswd = hashPassword(req.password)

        addMail = Mail(
            from_mail = req.from_mail,
            to_mail = req.to_mail,
            username = req.username,
            password = hashedpasswd,
            smtp_server = req.smtp_server,
            smtp_mail = req.smtp_mail,
            smtp_server_port = req.smtp_server_port,
            subject = req.subject,
            body = req.body
        )
        db.add(addMail)
        db.commit()
        return {"error": False, "message": "success"}
    
    except Exception as e: 
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")   
    

@router.get('/getMails')
async def allMails(db:db_dependency):
    Mails = db.query(Mail).all()
    return Mails


@router.get('/getMail/{mailId}')
async def mailById(mailId:int,db:db_dependency):
    try:
        mailSetup = db.query(Mail).filter(Mail.id == mailId).first()

        if not mailSetup:
            return {"error": True, "message": "No Mail Setup found"}
        return mailSetup
    
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")   

@router.delete('/deleteMail/{mailId}')
async def deleteMail(mailId: int, db: db_dependency):
    try:
        mailSetup = db.query(Mail).filter(Mail.id == mailId).first()

        if not mailSetup:
            return {"error": True, "message": "No Mail Setup found"}

        db.delete(mailSetup)
        db.commit()
        return {"error": False, "message": "succcess"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")


@router.put('/updateMail/{mailId}')
async def updateMail(mailId: int, req:MailSchema, db:db_dependency):
    try:
        mailSetup = db.query(Mail).filter(Mail.id == mailId).first()

        if not mailSetup:
            return {"error": True, "message": "No Mail Setup found"}
        
        hashedpasswd = hashPassword(req.password)
        
        mailSetup.from_mail = req.from_mail
        mailSetup.to_mail = req.to_mail
        mailSetup.username = req.username
        mailSetup.password = hashedpasswd
        mailSetup.smtp_server = req.smtp_server
        mailSetup.smtp_mail = req.smtp_mail
        mailSetup.smtp_server_port = req.smtp_server_port
        mailSetup.subject = req.subject
        mailSetup.body = req.body


        db.commit()
        return {"error": False, "message": "Updated successfully"}
    
    except Exception as e: 
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")

@router.post("/sendMail")
async def send_mail(req: MailSchema, db: db_dependency):
    try:
        result = mail_service.send_mail(
            from_mail=req.from_mail,
            to_mail=req.to_mail,
            subject=req.subject,
            body=req.body
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")


# @router.post("/sendMail/")
# async def send_email(request: EmailRequest):
    response = mail_service.send_email(
        from_email=request.from_mail,
        to_email=request.to_mail,
        subject=request.subject,
        body=request.body
    )
    if "successfully" not in response:
        raise HTTPException(status_code=500, detail=response)
    return {"message": response}

