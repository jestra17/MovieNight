import sqlite3

conn = sqlite3.connect('MovieDB.db')
c = conn.cursor()


def creat_db():
    c.execute("""CREATE TABLE IF NOT EXISTS MovieTB (
                                                ID INTEGER,
                                                TITLE TEXT,
                                                GENRE TEXT,
                                                DESCRIPTION TEXT,
                                                POSTER TEXT,
                                                RELEASE_DATE TEXT,
                                                STATUS TEXT,
                                                IMDB_LINK TEXT)""")


conn.commit()


def drop_M_TB():
    c.execute("DROP TABLE MovieTB")


def select(title):
    c.execute("SELECT ID, TITLE FROM MovieTB WHERE :TITLE = title" , {'TITLE' : title})
    print(c.fetchall())


def insert(m_id, title, genre, desc, poster, r_date, status, imdb_link):
    s = ""
    for item in genre:
        s = s + "," + item
    genre = s[1:len(s)]
    c.execute(
        "INSERT INTO MovieTB VALUES (:ID, :TITLE, :GENRE, :DESCRIPTION, :POSTER, :RELEASE_DATE, :STATUS, :IMDB_LINK)",
        {'ID': m_id, 'TITLE': title.lower(), 'GENRE': genre, 'DESCRIPTION': desc, 'POSTER': poster, 'RELEASE_DATE': r_date
            , 'STATUS': status, 'IMDB_LINK': imdb_link})
    conn.commit()


def closing_the_connection():
    conn.close()
