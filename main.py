import sqlite3

MAX_WORD_SIZE = 100
MAX_DESCRIPTION_SIZE = 250


def insert_word(word, definition):
    cursor.execute('Insert into Dictionary (Word, Definition) values (?, ?)', (word, definition))
    connection.commit()


def search_word(word):
    return cursor.execute('Select * from Dictionary where Word = ?', (word,)).fetchone()


def seed():
    words = [
        {'word': 'Xopa', 'definition': 'Forma coloquial de decir Hola.'},
        {'word': 'Tongo', 'definition': 'Forma coloquial de decir Policia.'},
    ]

    for word in words:
        result = search_word(word['word'])

        if result is not None:
            continue

        insert_word(word['word'], word['definition'])


def add():
    word = input('Palabra: ')

    if validate(word, 'Palabra', MAX_WORD_SIZE) is False:
        return

    description = input('Descripción: ')

    if validate(description, 'Descripción', MAX_DESCRIPTION_SIZE) is False:
        return

    try:
        insert_word(word, description)
    except sqlite3.IntegrityError as e:
        print(e)


def show(result):
    print(f'{result[0]}: {result[1]}')


def search():
    word = input('Palabra: ')

    if validate(word, 'Palabra', MAX_WORD_SIZE) is False:
        return

    result = search_word(word)

    if result is None:
        print(f'La palabra {word} no existe en el diccionario.')
        return

    show(result)


def validate(field, key, size):
    field_len = len(field)

    if field_len == 0 or field == '':
        print(f'Debe de llenar el campo {key}.')
        return False
    elif field_len > size:
        print(f'El campo {key} excede la cantidad de caracteres: {size}')
        return False
    return True


def edit():
    word = input('Palabra: ')

    if validate(word, 'Palabra', MAX_WORD_SIZE) is False:
        return None

    description = input('Descripción: ')

    if validate(description, 'Descripción', MAX_DESCRIPTION_SIZE) is False:
        return None

    try:
        cursor.execute('Update Dictionary set Definition = ? where Word = ?', (word, description))
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(e)


def delete():
    word = input('Palabra: ')

    if validate(word, 'Palabra', 50) is False:
        return None

    try:
        cursor.execute('Delete from Dictionary where Word = ?', (word,))
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(e)


def show_all():
    words = cursor.execute('Select * from Dictionary')

    for word in words:
        show(word)


if __name__ == '__main__':
    connection = sqlite3.Connection('slangs.db')

    cursor = connection.cursor()

    cursor.execute(f"""Create Table If Not Exists Dictionary 
        (Word Varchar({MAX_WORD_SIZE}) Unique, Definition Varchar({MAX_DESCRIPTION_SIZE}))
        """)
    connection.commit()

    seed()

    while True:
        print('Menu')
        print('1- Agregar')
        print('2- Buscar')
        print('3- Editar')
        print('4- Borrar')
        print('5- Mostrar')
        print('6- Salir')
        option = int(input('Opcion (1-6): '))

        if option == 1:
            add()
        elif option == 2:
            search()
        elif option == 3:
            edit()
        elif option == 4:
            delete()
        elif option == 5:
            show_all()
        else:
            break

        should_continue = input('Desea continuar (s/N)?: ')

        if should_continue.lower() != 's':
            break




