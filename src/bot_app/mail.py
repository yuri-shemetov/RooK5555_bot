import email
import imaplib
import io

from bot_app.my_local_settings import ADDR_FROM, PASSWORD_FOR_EMAIL

from datetime import datetime
from decimal import *
from os import mkdir, path


def get_new_email(price, servername="imap.yandex.ru"):
    subject = "Your SSL Certificate"
    mail = imaplib.IMAP4_SSL(servername)
    mail.login(ADDR_FROM, PASSWORD_FOR_EMAIL)
    mail.list()
    mail.select("INBOX")
    request_price = Decimal(int(price))
    BODY = f'UNSEEN BODY "{request_price}"'
    (status, data) = mail.search(None, f"{BODY}")
    date_message = datetime.strftime(datetime.now(), "%y_%m_%d-%H-%M-%S")
    money = 0

    if data != [b""]:
        for num in data[0].split():
            status, email_data = mail.fetch(num, "(RFC822)")
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode("utf-8")
            email_message = email.message_from_string(raw_email_string)

            # Header Details
            date_tuple = email.utils.parsedate_tz(email_message["Date"])
            if date_tuple:
                local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                local_message_date = "%s" % (
                    str(local_date.strftime("%a, %d %b %Y %H:%M:%S"))
                )
            email_from = str(
                email.header.make_header(
                    email.header.decode_header(email_message["From"])
                )
            )
            email_to = str(
                email.header.make_header(
                    email.header.decode_header(email_message["To"])
                )
            )
            subject = str(
                email.header.make_header(
                    email.header.decode_header(email_message["Subject"])
                )
            )

            if (
                subject == "4.6812/Перевод (Поступление)"
            ):  # <--- replace the text, A-bank
                # Body details
                for part in email_message.walk():
                    if (
                        part.get_content_type() == "text/plain"
                        or part.get_content_type() == "text/html"
                    ):
                        body = part.get_payload(decode=True)
                        
                        if not path.exists("message/"):
                            mkdir(f"message/")

                        file_name = "message/" + f"{date_message}.txt"
                        output_file = open(file_name, "w", encoding="utf-8")
                        output_file.write(
                            "From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s"
                            % (
                                email_from,
                                email_to,
                                local_message_date,
                                subject,
                                body.decode("utf-8"),
                            )
                        )
                        output_file.close()
                        try:
                            with io.open(
                                file_name, mode="r", encoding="utf-8"
                            ) as f_obj:
                                contents = f_obj.read()
                                words = contents.split()
                                i = 0
                                for word in words:
                                    i += 1
                                    if (
                                        word == "Успешно"
                                    ):  # <--- replace the text, A-bank
                                        money = words[i]
                                        money = money[6:]
                                return money
                        except:
                            return money
                    else:
                        continue
            else:
                return money
    else:
        return money

    mail.close()
