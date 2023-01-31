import datetime
import sys
import traceback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from customError import EmailError
from util import getValueIfExist


class EmailClient:
    def __init__(self, configJson) -> None:

        self.scriptName = sys.argv[0]  # get the script path
        adminFields = getValueIfExist("admin", configJson)  # get admin dic

        self.adminEmail = getValueIfExist(
            "errorRecipients", adminFields
        )  # get admin email

        emailFields = getValueIfExist("email", configJson)  # get email dic

        self.eMailFrom = getValueIfExist("from", emailFields)  # get from email address

        self.eMailTo = getValueIfExist(
            "recipients", emailFields
        )  # get to email address

        self.serverInfo = getValueIfExist(
            "server", emailFields
        )  # get smtp server address
        self.port = getValueIfExist("port", emailFields)  # get smpt port

        self.eMailSubject = getValueIfExist("subject", emailFields)  # get subject text
        self.password = getValueIfExist(
            "password", emailFields
        )  # get password. This is not a good practice to place the password in a config file, but for the sake of this assignment, I am placing it there.

        # self.eMailFrom = os.environ.get("APP_EMAIL") # get email from env variable
        # self.password = os.environ.get("APP_EMAIL_PASS") # get pass from env variable

    def sendInspectionEmail(self, message):
        """email the inspection report

        Args:
            message ([str]):
        """
        try:
            self._sendEmail(
                self.eMailTo,
                message,
                self.eMailFrom,
                self.eMailSubject,
            )

        except smtplib.SMTPResponseException:
            # raise custom error to to capture in the main module
            raise EmailError(message="Sending email failed")

    def _sendEmail(self, eMailTo, messagetext, eMailFrom, eMailSubject):
        """send email

        Args:
            eMailTo (str): to email
            messagetext (str): email body
            eMailFrom (str): from email
            eMailSubject (str): email subject

        Raises:
            EmailError: custom error
        """

        if eMailTo[0].index("@") > 0:
            # Check if any email address in To field is present
            emailMessage = MIMEMultipart()  # multipart if we want to send attachment
            emailText = MIMEText(
                messagetext, "html", _charset="UTF-8"
            )  # Make sure message format is html

            emailMessage["From"] = eMailFrom  # set email from
            emailMessage["To"] = ", ".join(eMailTo)  # set to emails list
            emailMessage["Subject"] = eMailSubject  # set email subject
            emailMessage.attach(emailText)  # Add the message body

            # Connect to mail server
            with smtplib.SMTP(self.serverInfo, self.port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.eMailFrom, self.password)
                server.sendmail(
                    eMailFrom, list(eMailTo), emailMessage.as_string()
                )  # Send the email
                server.quit()

    def SendErrorMessage(self, message):
        try:
            errorSubjectLine = "Error in the drainage inspection daily summary script"
            errorMessage = f"{message} - {traceback.format_exc()}"
            # Email body with current date time
            ErrorBody = f'{self.scriptName} Failed at:{str(datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"))}<br>{errorMessage}'

            self._sendEmail(
                self.adminEmail,
                ErrorBody,
                self.eMailFrom,
                errorSubjectLine,
            )
        except smtplib.SMTPResponseException:
            # if couldn't send the error email, quit the script since the log is already created in the main module
            raise SystemExit
