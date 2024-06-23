import sqlite3


class SQLighter:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения, если БД не существует - создаем ее"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS subscriptions (id INTEGER AUTO_INCREMENT PRIMARY KEY, \
                        user_id VARCHAR (255) NOT NULL, reviewed BOOLEAN, approve BOOLEAN, \
                        price DECIMAL, loyalty_price DECIMAL, rate CHAR (10), translation DECIMAL, address CHAR, \
                        photo BLOB, created CHAR, start_timestamp INT, total_amount DECIMAL, name_bank CHAR (30))"
        )

    def subscriber_exists(self, user_id):
        """Check user"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, rate, price, translation, created, start_timestamp, reviewed=True):
        """Add a new user"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `subscriptions` (`user_id`, 'reviewed', 'rate', 'price', 'translation', 'created', 'start_timestamp') "
                "VALUES(?, ?, ?, ?, ?, ?, ?)",
                (user_id, reviewed, rate, price, translation, created, start_timestamp),
            )

    def update_name_bank(self, user_id, name_bank):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `name_bank` = ?"
                "WHERE `user_id` = ?",
                (name_bank, user_id),
            )


    def update_subscription(self, user_id, rate, price, translation, created, start_timestamp):
        """Update user"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `rate` = ?, `price` = ?, 'translation' = ?, 'created' = ?, 'start_timestamp' = ? "
                "WHERE `user_id` = ?",
                (rate, price, translation, created, start_timestamp, user_id),
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
        
    def update_subscription_price(self, user_id, price):
        """Update price"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `price` = ? WHERE `user_id` = ?",
                (price, user_id),
            )
        
    def update_subscription_loyalty_price(self, user_id, loyalty_price):
        """Update loyalty price"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `loyalty_price` = ? WHERE `user_id` = ?",
                (loyalty_price, user_id),
            )
    
    def update_subscription_total_amount(self, user_id, total_amount):
        """Update total_amount"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `total_amount` = ? WHERE `user_id` = ?",
                (total_amount, user_id),
            )

    def get_subscriptions_all_price(self, user_id):
        """Get all price"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `price` FROM `subscriptions` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
    
    def get_subscriptions_all_loyalty_price(self, user_id):
        """Get all loyalty price"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `loyalty_price` FROM `subscriptions` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
    
    def get_subscriptions_total_amount(self, user_id):
        """Get total amount for loyalty program"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `total_amount` FROM `subscriptions` WHERE `user_id` = ?", (user_id,)
            ).fetchone()

    def get_subscriptions_translation(self, user_id):
        """Get coins"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `translation`, `rate` FROM `subscriptions` WHERE `user_id` = ?",
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

    def get_subscriptions_start_timestamp(self, user_id):
        """Get start_timestamp"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `start_timestamp` FROM `subscriptions` WHERE `user_id` = ?",
                (user_id,),
            ).fetchall()

    def get_name_bank(self, user_id):
        """Get name bank"""
        with self.connection:
            return self.cursor.execute(
                "SELECT `name_bank` FROM `subscriptions` WHERE `user_id`= ?",
                (user_id,),
            ).fetchone()

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


class Bank:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS bank ( \
                        id INTEGER PRIMARY KEY, \
                        name VARCHAR (30) NOT NULL,\
                        requisiters TEXT NOT NULL,\
                        amount DECIMAL DEFAULT 0,\
                        is_active BOOLEAN DEFAULT (True),\
                        is_only_day BOOLEAN,\
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP)"
        )


    def add_bank_name(self, name, requisiters):
        """Add bank name"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `bank` (`name`, 'requisiters') "
                "VALUES(?, ?)",
                (name, requisiters),
            )

    def get_full_data(self, is_only_day=True):
        """Get only requisiters, is_only_day, amount, name"""
        with self.connection:
            if is_only_day:
                return self.cursor.execute(
                    "SELECT `requisiters`, `is_only_day`, `amount`, `name` FROM `bank` WHERE `is_active` = true",
                ).fetchall()
            else:
                return self.cursor.execute(
                    "SELECT `requisiters`, `is_only_day`, `amount`, `name` FROM `bank` WHERE `is_active` = true AND `is_only_day` = false",
                ).fetchall()
            
    def get_name_bank(self, name_bank):
        with self.connection:
            return self.cursor.execute(
                "SELECT `id` FROM `bank` WHERE `name` = ?",
                (name_bank,),
            ).fetchone()

            
    def get_amount_from_bank(self, name_bank):
        with self.connection:
            return self.cursor.execute(
                "SELECT `amount` FROM `bank` WHERE `name` = ?",
                (name_bank,),
            ).fetchone()
        
    def get_total(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT SUM(`amount`) FROM `bank` WHERE `is_active` = true",
            ).fetchone()


    def update_requisiters(self, requisiters):
        """Add bank name"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `bank` SET `requisiters` = ?"
                "WHERE `requisiters` = ? ",
                (requisiters, "new"),
            )

    def update_is_only_day(self, is_only_day):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `bank` SET `is_only_day` = ?"
                "WHERE is_only_day IS NULL ",
                (is_only_day,),
            )
        
    def update_amount_zero(self):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `bank` SET `amount` = 0"
            )
        
    def update_amount_from_bank(self, amount, name_bank):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `bank` SET `amount` = ? WHERE `name` = ?",
                (amount, name_bank,),
            )
        
    def remove_requisiters(self, name_bank):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM `bank`"
                "WHERE name = ? ",
                (name_bank,),
            )

    def close(self):
        """Close DB"""
        self.connection.close()