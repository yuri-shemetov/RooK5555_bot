import csv
import yadisk

from bot_app.app import db
from bot_app.my_local_settings import yadisk_id, ya_secret, yadisk_token
from datetime import datetime
from os import mkdir, path


def save_to_yadisk(id_user, path_jpg):
    y = yadisk.YaDisk(yadisk_id, ya_secret, yadisk_token)
    date = datetime.strftime(datetime.now(), "%y_%m_%d__%H-%M-%S")
    mounth = datetime.strftime(datetime.now(), "%y_%m")
    order = datetime.strftime(datetime.now(), "%d/%m/%y-%H:%M:%S")
    byn = db.get_subscriptions_all_price(id_user)[0][0]

    if not y.exists(f"/{mounth}"):
        y.mkdir(f"/{mounth}")

    if not y.exists(f"/{mounth}/00_PHOTO"):
        y.mkdir(f"/{mounth}/00_PHOTO")

    if not y.exists(f"/{mounth}/01_USERS"):
        y.mkdir(f"/{mounth}/01_USERS")

    if not y.exists(f"/{mounth}/01_USERS/ID_{id_user}"):
        y.mkdir(f"/{mounth}/01_USERS/ID_{id_user}")

    if not path.exists(f"{mounth}/"):
        mkdir(f"{mounth}/")

    myData = [
        [
            f"{order} ",
            f"id: ",
            f"{id_user} ",
            f"BYN: ",
            f"{byn} ",
            f"path_to_photo: ",
            f"{date}_id{id_user}.jpg",
        ]
    ]
    path_csv = f"{mounth}/My_DATA.csv"

    with open(path_jpg, "rb") as photo:
        y.upload(photo, f"/{mounth}/00_PHOTO/{date}_id{id_user}.jpg")

    with open(path_csv, "a+") as file_csv:
        writer = csv.writer(file_csv)
        writer.writerows(myData)

    with open(path_csv, "rb+") as file_csv:
        try:
            y.remove(f"/{mounth}/00_MY_DATA_{mounth}.csv", permanently=True)
        except:
            pass
        y.upload(file_csv, f"/{mounth}/00_MY_DATA_{mounth}.csv")
    
    with open(path_jpg, "rb") as photo:
        y.upload(photo, f"/{mounth}/01_USERS/ID_{id_user}/{date}_id{id_user}.jpg")


def save_to_yadisk_wallet(username, lastname, id_user, user_message):
    y = yadisk.YaDisk(yadisk_id, ya_secret, yadisk_token)
    date = datetime.strftime(datetime.now(), "%y_%m_%d__%H-%M-%S")
    mounth = datetime.strftime(datetime.now(), "%y_%m")

    if not path.exists(f"wallet/"):
        mkdir(f"wallet/")

    if not y.exists(f"/{mounth}/00_WALLET"):
        y.mkdir(f"/{mounth}/00_WALLET")

    file_name = "wallet/" + f"{date}.txt"
    with open(file_name, "w+") as message:
        message.write(f"{user_message}")

    with open(file_name, "rb") as message:
        y.upload(
            message,
            f"/{mounth}/00_WALLET/{date}_id{id_user}_[{username}_{lastname}].txt",
        )
