import psycopg2

#Функция, создающая структуру БД (таблицы)

def create_db(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
           id SERIAL PRIMARY KEY,
           first_name VARCHAR(25) NOT NULL,
           last_name VARCHAR(25) NOT NULL,
           e_mail  VARCHAR(40) NOT NULL);
           """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients_phones(
            id SERIAL PRIMARY KEY,
            phone_number integer UNIQUE,
            client_id INTEGER REFERENCES clients(id));
            """)


#Функция, позволяющая добавить нового клиента

def add_client(cur, first_name, last_name, e_mail, phone_number=None, client_id=None):
    cur.execute("""
            INSERT INTO clients (first_name, last_name, e_mail) VALUES (%s, %s, %s);
                """, (first_name, last_name, e_mail))

    if phone_number is not None:
        cur.execute("""
                INSERT INTO clients_phones (client_id, phone_number) VALUES (%s, %s);
                    """, (client_id, phone_number))


#Функция, позволяющая добавить телефон для существующего клиента

def add_phone(cur, client_id, phone_number):
    cur.execute("""
       INSERT INTO clients_phones(client_id, phone_number)  VALUES (%s, %s);
                    """, (client_id, phone_number))

#Функция, позволяющая изменить данные о клиенте

def update_clients(cur, id, first_name, last_name, e_mail, phone_number=None):
    print('Выберите команду для внесения изменений:\n'
          'name - изменить имя, lastname - фамилия, email - эл.почта, phone = номер телефона')
    while True:
        user_command = input()
        if user_command == 'name':
            input_id = input('Введите id клиента, для которого необходимо внесьи изменения')
            input_new_name = input('Введите новое имя')
            cur.execute("""
                        UPDATE clients SET first_name=%s WHERE id=%s; 
                            """, (input_new_name, input_id))
            print(cur.fetchall())

        elif user_command == 'lastname':
            input_id_ = input('Введите id клиента, для которого необходимо внесьи изменения')
            input_new_lastname = input('Введите новую фамилию')
            cur.execute("""
                        UPDATE clients SET last_name=%s WHERE id=%s; 
                            """, (input_new_lastname, input_id_))
            break

        elif user_command == 'e_mail':
            input_id_1 = input('Введите id клиента, для которого необходимо внесьи изменения')
            input_new_email = input('Введите новую эл.почту')
            cur.execute("""
                        UPDATE clients SET e_mail=%s WHERE id=%s; 
                            """, (input_new_email, input_id_1))
            break

        elif user_command == 'phone_number':
            input_current_phone = input('Введите номер, который необходимо изменить:')
            input_new_phone = input('Введите новый телефон')
            cur.execute("""
                        UPDATE clients_phones SET phone_number=%s WHERE phone_number=%s; 
                            """, (input_new_phone, input_current_phone))
            break
    else:
        print('Ошибка ввода. Проверьте правильность ввода данных.')

#Функция, позволяющая удалить телефон для существующего клиента

def del_phone(cur):
    id_to_delete = input('Введите id клиента, номер телефона которого хотите удалить:')
    phone_to_delete = input('Введите номер, который хотите удалить:')
    cur.execute("""
                   DELETE FROM  clients_phones  WHERE client_id=%s AND phone_number=%s
                """, (id_to_delete, phone_to_delete))

#Функция, позволяющая удалить существующего клиента

def del_client(cur):
    client_to_delete = input('Введите id клиента, которого хотите удалить:')
    cur.execute("""
                DELETE FROM  clients  WHERE client_id=%s;
                """, (client_to_delete))

#Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)

def find_client(cur):
    print('Введите параметр, по которому осуществлять поиск:\n'
          'name - по имени, lastname - по фамилии, email - по эл.почте, phone = по номеру телефона')
    while True:
        search_command = int(input('Введите команду для поиска:'))
        if search_command == 1:
            search_by_name = input('Ввtдите имя для поиска: ')
            cur.execute("""
            SELECT id, first_name, last_name, e_mail, phone_number FROM clients AS c
            LEFT JOIN clients_phones AS cp ON cp.client_id = c.id
            WHERE first_name=%s
            """, (search_by_name))
            print(cur.fetchall())
        elif search_command == 2:
            search_by_lastname = input('Введите фамилию для поиска: ')
            cur.execute("""
            SELECT id, first_name, last_name, e_mail, phone_number FROM clients AS c
            LEFT JOIN clients_phones AS cp ON cp.client_id = c.id
            WHERE last_name=%s
            """, (search_by_lastname))
            print(cur.fetchall())
        elif search_command == 3:
            search_by_e_mail = input('Введите e_mail для поиска: ')
            cur.execute("""
            SELECT id, first_name, last_name, e_mail, phone_number FROM clients AS c
            LEFT JOIN clients_phones AS cp ON cp.client_id = c.id
            WHERE e_mail=%s
            """, (search_by_e_mail))
            print(cur.fetchall())
        elif search_command == 4:
            search_by_phone = input('Введите e_mail для поиска: ')
            cur.execute("""
            SELECT id, first_name, last_name, e_mail, phone_number FROM clients AS c
            LEFT JOIN clients_phones AS cp ON cp.client_id = c.id
            WHERE e_mail=%s
            """, (search_by_phone))
            print(cur.fetchall())
    else:
        print('Ошибка ввода. Проверьте правильность ввода данных.')
with psycopg2.connect( user="postgres", password="Guj4_kow", database="clients") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        add_client(cur, 'Oleg', 'Ivanov', 'ol@iv.com')
        add_client(cur, 'Petr', 'Stepanov', 'pet@st.com')
        add_client(cur, 'Elena', 'Petrova', 'el@pet.com')
        # add_phone(cur, '1', '123456789')
        # add_phone(cur, '2', '987654321')
        # add_phone(cur, '3', '132436475')

conn.close()