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
    if data == [b""] and len(str(price)) == 4:
        request_price_plus_space = str(price)[1:]
        BODY = f'UNSEEN BODY "{request_price_plus_space}"'
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
                subject == "SMS-Extra: [STATUSBANK] -> [375292929301]"
            ):  # <--- replace the text, SMS from STATUSBANK
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
                                i = 1
                                for word in words:
                                    i += 1
                                    if (
                                        word == "Popolnenie" and len(words[i]) != 1
                                    ):  # <--- replace the text, STATUSBANK
                                        money = words[i].replace(',', '.')
                                        return money
                                    elif (
                                        word == "Popolnenie" and len(words[i]) == 1
                                    ):  # <--- replace the text, STATUSBANK
                                        parameters = [words[i], words[i+1].replace(',', '.')]
                                        money = "".join(parameters)
                                        return money
                                return money
                        except:
                            return money
                    else:
                        continue
            elif (
                subject == "SMS-Extra: [Technobank] -> [375292929301]"
            ):  # <--- replace the text, SMS from Technobank
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
                                        word == "Credit"
                                    ):  # <--- replace the text, Technobank
                                        money = words[i][1:]
                                        return money
                                return money

                        except:
                            return money
                    else:
                        continue

            elif (
                subject == "SMS-Extra: [Bank_VTB] -> [375292929301]"
            ):  # <--- replace the text, SMS from Bank_VTB
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
                                        word == "POPOLNENIE"
                                    ):  # <--- replace the text, Bank_VTB
                                        money = words[i]
                                        return money
                                return money

                        except:
                            return money
                    else:
                        continue
            elif (
                subject == "SMS-Extra: [BNB-BANK] -> [375292929301]"
            ):  # <--- replace the text, SMS from BNB-BANK
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
                                        word == "Zachislen"
                                    ):  # <--- replace the text, BNB-BANK
                                        money = words[i+1]
                                        return money
                                return money

                        except:
                            return money
                    else:
                        continue
            elif (
                subject == "SMS-Extra: [BelVEB24.BY] -> [375292929301]"
            ):  # <--- replace the text, SMS from BelVEB24.BY
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
                                        word == "Credit"
                                    ):  # <--- replace the text, BelVEB24.BY
                                        money = words[i]
                                        return money[1:]
                                return money

                        except:
                            return money
                    else:
                        continue
            elif (
                subject == "SMS-Extra: [BTA_BANK] -> [375292929301]"
            ):  # <--- replace the text, SMS from BTA_BANK
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
                                        word == "CREDIT"
                                    ):  # <--- replace the text, BTA_BANK
                                        money = words[i]
                                        return money
                                return money

                        except:
                            return money
                    else:
                        continue
            elif (
                subject == "SMS-Extra: [BSB-Bank] -> [375292929301]"
            ):  # <--- replace the text, SMS from BSB-Bank
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
                                        word == "Popolnenie" and word[i] == "Uspeshno"
                                    ):  # <--- replace the text, BSB-Bank
                                        money = words[i+4]
                                        return money
                                return money

                        except:
                            return money
                    else:
                        continue
            # elif (
            #     subject == "SMS-Extra: [MTBANK] -> [375292929301]"
            # ):  # <--- replace the text, SMS from MTBANK
            #     # Body details
            #     for part in email_message.walk():
            #         if (
            #             part.get_content_type() == "text/plain"
            #             or part.get_content_type() == "text/html"
            #         ):
            #             body = part.get_payload(decode=True)
                        
            #             if not path.exists("message/"):
            #                 mkdir(f"message/")

            #             file_name = "message/" + f"{date_message}.txt"
            #             output_file = open(file_name, "w", encoding="utf-8")
            #             output_file.write(
            #                 "From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s"
            #                 % (
            #                     email_from,
            #                     email_to,
            #                     local_message_date,
            #                     subject,
            #                     body.decode("utf-8"),
            #                 )
            #             )
            #             output_file.close()
            #             try:
            #                 with io.open(
            #                     file_name, mode="r", encoding="utf-8"
            #                 ) as f_obj:
            #                     contents = f_obj.read()
            #                     words = contents.split()
            #                     i = 0
            #                     for word in words:
            #                         i += 1
            #                         if (
            #                             word == "zachisleno" and len(words[i]) != 1
            #                         ):  # <--- replace the text, MTBANK
            #                             money = words[i]
            #                             return money
            #                         elif (
            #                             word == "zachisleno" and len(words[i]) == 1
            #                         ):
            #                             parameters = [words[i], words[i+1]]
            #                             money = "".join(parameters)
            #                             return money
            #                     return money

            #             except:
            #                 return money
            #         else:
            #             continue
            else:
                return money
    else:
        return money

    mail.close()
