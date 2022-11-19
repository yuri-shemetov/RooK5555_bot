import sqlite3


class SQLighter:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения, если БД не существует - создаем ее"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS subscriptions (id INTEGER AUTO_INCREMENT PRIMARY KEY, \
                        user_id VARCHAR (255) NOT NULL, reviewed BOOLEAN, approve BOOLEAN, \
                        price DECIMAL, rate CHAR (3), translation DECIMAL, address CHAR, photo BLOB, created CHAR)"
        )

    def subscriber_exists(self, user_id):
        """Check user"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, rate, price, translation, created, reviewed=True):
        """Add a new user"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `subscriptions` (`user_id`, 'reviewed', 'rate', 'price', 'translation', 'created') "
                "VALUES(?, ?, ?, ?, ?, ?)",
                (user_id, reviewed, rate, price, translation, created),
            )

    def update_subscription(self, user_id, rate, price, translation, created):
        """Update user"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `rate` = ?, `price` = ?, 'translation' = ?, 'created' = ? "
                "WHERE `user_id` = ?",
                (rate, price, translation, created, user_id),
            )

    def update_subscription_address_reviewed_and_approve(
        self, user_id, address, reviewed=False, approve=None
    ):
        """Update address, reviewed and approve"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `address` = ?, `reviewed`= ?, `approve` = ? WHERE `user_id` = ?",
                (address, reviewed, approve, user_id),
            )

    def update_subscription_reviewed_and_approve(
        self, user_id, reviewed=True, approve=None
    ):
        """Update reviewed and approve"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `reviewed` = ?, `approve` = ? WHERE `user_id` = ?",
                (reviewed, approve, user_id),
            )

    def update_subscription_photo(self, user_id, photo):
        """Update photo"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `photo` = ? WHERE `user_id` = ?",
                (photo, user_id),
            )

    def get_subscriptions_all_price(self, user_id):
        """Get all price"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `price` FROM `subscriptions` WHERE `user_id` = ?", (user_id,)
            ).fetchall()

    def get_subscriptions_translation(self, user_id):
        """Get bitcoins"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `translation` FROM `subscriptions` WHERE `user_id` = ?",
                (user_id,),
            ).fetchall()

    def get_subscriptions_created(self, user_id):
        """Get creation date"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `created` FROM `subscriptions` WHERE `user_id` = ?",
                (user_id,),
            ).fetchall()

    def get_subscriptions_photo_price(self, user_id):
        """Get photo, price"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `photo`, `price` FROM `subscriptions` WHERE `user_id` = ?",
                (user_id,),
            ).fetchall()

    def get_subscriptions_approve(self, user_id):
        """Get approve"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `approve` FROM `subscriptions` WHERE `user_id` = ?", (user_id,)
            ).fetchall()

    def get_subscriptions_reviewed(self, user_id):
        """Get reviewed"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `reviewed` FROM `subscriptions` WHERE `user_id` = ?", (user_id,)
            ).fetchall()

    def close(self):
        """Close DB"""
        self.connection.close()


class Applications:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS applications ( \
                        id INTEGER AUTO_INCREMENT PRIMARY KEY, \
                        user_id VARCHAR (255) NOT NULL,\
                        application_submitted BOOLEAN DEFAULT (False))"
        )

    def get_or_create_application_submitted(self, user_id):
        """Get or create application"""
        with self.connection:
            if self.cursor.execute(
                "SELECT * FROM `applications` WHERE `user_id` = ?", (user_id,)
            ).fetchall():
                return self.cursor.execute(
                    "SELECT `application_submitted` FROM `applications` WHERE `user_id` = ?",
                    (user_id,),
                ).fetchall()
            else:
                self.cursor.execute(
                    "INSERT INTO `applications` (`user_id`) VALUES (?)", (user_id,)
                )
                return self.cursor.execute(
                    "SELECT `application_submitted` FROM `applications` WHERE `user_id` = ?",
                    (user_id,),
                ).fetchall()

    def update_application_submitted(self, user_id, application_submitted=True):
        """Update application"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `applications` SET `application_submitted` = ? WHERE `user_id` = ?",
                (application_submitted, user_id),
            )

    def close(self):
        """Close DB"""
        self.connection.close()
