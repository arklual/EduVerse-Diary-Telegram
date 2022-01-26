import psycopg2

class DBFile():
    def __init__(self):
        # Подключаемся к БД
        self.conn = psycopg2.connect(
            user="iwxyjkkksqcyfo",                      
            password="d990545bc24ecc5a8d25a42c9af5a44793a467726567b9316302123ab5cb668b",
            host="ec2-3-224-157-224.compute-1.amazonaws.com",
            port="5432",
            database="d304kv08jp0b71"
        )
        self.cursor = self.conn.cursor()
        #self.cursor.execute("""DROP TABLE public.students;""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS public.students
        (   
            id serial NOT NULL,
            user_id integer NOT NULL,
            subscription_status boolean NOT NULL DEFAULT true,
            leaved_review boolean NOT NULL DEFAULT false,
            join_date timestamptz NOT NULL DEFAULT NOW(),
            get_emails boolean NOT NULL DEFAULT true,
            school text,
            school_id text,
            locality text,
            locality_id text,
            login_text text,
            password_text text,
            CONSTRAINT students_primarykey PRIMARY KEY (id)
        );
        ALTER TABLE students ADD CONSTRAINT login_utext UNIQUE(login_text);

        """)
    
    def get_subs(self, status):
        with self.conn:
            self.cursor.execute(f"""SELECT * FROM students WHERE subscription_status = {status};""")
            return self.cursor.fetchall()

    def subscriber_exists(self, user_id):
        with self.conn:
            user_id = str(user_id)
            self.cursor.execute(f"""SELECT * FROM public.students WHERE user_id = {user_id};""")
            return bool(len(self.cursor.fetchall()))
            
    def is_subscribed(self, user_id, sub_status = True):
        with self.conn:
            user_id = str(user_id)
            self.cursor.execute(f"""SELECT * FROM public.students WHERE user_id = {user_id} AND status = {sub_status}""")
            return bool(len(self.cursor.fetchall()))

    def add_subscriber(self, user_id, status = True):
        with self.conn:
            user_id = str(user_id)
            return self.cursor.execute(f"""INSERT INTO students (user_id, subscription_status) VALUES ({user_id}, {status});""")
    
    def update_subscription(self, user_id, status):
        user_id = str(user_id)
        return self.cursor.execute(f"""UPDATE students SET subscription_status = {status} WHERE user_id = {user_id};""")

    def is_user_subcribes_bot_but_not_subcribes_email(self, user_id, email_status = False):
        with self.conn:
            user_id = str(user_id)
            self.cursor.execute(f"""SELECT * FROM public.students WHERE user_id = {user_id} AND get_emails = {email_status};""")
            return bool(len(self.cursor.fetchall()))

    def update_get_emails_status(self, user_id, sub_status, email_sub_status):
        user_id = str(user_id)
        return self.cursor.execute(f"""UPDATE students SET get_emails = {email_sub_status} WHERE user_id = {user_id} AND subscription_status = {sub_status}""")
    
    def signin(self, user_id, login, password, locality, locality_id, school, school_id):
        with self.conn:
            user_id = str(user_id)
            return self.cursor.execute(f"""INSERT INTO students(school, school_id, locality, locality_id, login_text, password_text) VALUES({school}, {school_id}, {locality}, {locality_id}, {login}, {password}) WHERE user_id = {user_id}""")

    def close(self):
        self.conn.close()
    

    