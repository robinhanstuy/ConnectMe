import sqlite3
import datetime
import random

import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/userdata.db"
dbfile = "data/userdata.db"
def createdb():
    db = initdb()
    c = db.cursor()
    c.execute('''CREATE TABLE if not exists users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    username TEXT,
    password TEXT,
    bio TEXT,
    position TEXT,
    interests TEXT,
        major TEXT,
        picpath TEXT
);''')
    c.execute('''CREATE TABLE if not exists msgs (
        id INTEGER PRIMARY KEY,
        user1 INTEGER,
        user2 INTEGER,
        text TEXT,
        time TEXT
    );''')
    c.execute('''CREATE TABLE if not exists swipes (
        id INTEGER PRIMARY KEY ,
        user1 INTEGER,
        user2 INTEGER
    );''')
    db.commit()
    db.close()
def initdb():
    db = sqlite3.connect(DATABASE_LINK)
    return db
def checkuser(user):
    db = initdb()
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (user, ))
    dupusers = c.fetchall()
    db.close()
    return len(dupusers) > 0
def getpassword(user):
    db = initdb()
    c = db.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (user, ))
    password = c.fetchone()[0]
    db.close()
    return password
def resetpassword(user, newpass):
    db = initdb()
    c = db.cursor()
    c.execute("UPDATE users SET password = ? WHERE username = ?", (newpass, user))
    db.commit()
    db.close()
def loginuser(user, password):
    db = initdb()
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, password))
    creds = c.fetchall()
    db.close()
    return len(creds) > 0
def newuser(name, user, password):
    db = initdb()
    c = db.cursor()
    c.execute("SELECT * FROM users")
    usrs = c.fetchall()
    if len(usrs) == 0:
        c.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?)", (0, name, user, password, "", "", "", "", ""))
    else:
        c.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?)", (len(usrs), name, user, password, "", "", "", "", ""))
    db.commit()
    db.close()
    return True
def fillqs(email, bio, pos, maj, intrsts):
    db = initdb()
    c = db.cursor()
    c.execute("UPDATE users SET bio = ?, position = ?, interests = ?, major = ? WHERE username = ?", (bio, pos, intrsts, maj, email))
    db.commit()
    db.close()
    return True
def fetchrand(user):
    db = initdb()
    c = db.cursor()
    swipes = getswipes(user)
    swipes = {int(s[2]) for s in swipes}
    c.execute("SELECT * FROM users WHERE id != ? ORDER BY RANDOM();", (user, ))
    pf = c.fetchall()
    i = 0
    while i < len(pf):
        if pf[i][0] in swipes:
            pf = pf[:i] + pf[i+1:]
            i -= 1
        i += 1
    db.close()
    if len(pf) > 0:
        return pf[0]
    else:
        return None
def getuser(user):
    db = initdb()
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ?;", (user, ))
    pf = c.fetchone()
    db.close()
    return pf

def getuserbyid(id):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE id = ?;", (id, ))

    pf = c.fetchone()

    db.close()
    return pf

def edituser(name, user, pos, maj, intrsts, bio, olduser):
    db = initdb()
    c = db.cursor()
    c.execute("UPDATE users SET name = ?, username = ?, bio = ?, position = ?, interests = ?, major = ? WHERE username = ?", (name, user, bio, pos, intrsts, maj, user))
    db.commit()
    db.close()
    return True
def getmsgs(user1, user2):
    db = initdb()
    c = db.cursor()
    c.execute("SELECT * FROM msgs WHERE user1 = ? AND user2 = ?", (user1, user2))
    msgs = c.fetchall()
    c.execute("SELECT * FROM msgs WHERE user1 = ? AND user2 = ?", (user2, user1))
    msgs.extend(c.fetchall())
    db.close()
    return msgs
def addmsg(txt, user1, user2):
    db = initdb()
    c = db.cursor()
    c.execute("SELECT * FROM msgs")
    msgs = c.fetchall()

    if len(msgs) == 0:
        c.execute("INSERT INTO msgs VALUES(?,?,?,?,?)", (0, user1, user2, txt, str(datetime.datetime.now())))
    else:
        c.execute("INSERT INTO msgs VALUES(?,?,?,?,?)", (len(msgs), user1, user2, txt, str(datetime.datetime.now())))
    c.execute("SELECT * FROM msgs")
    msgs = c.fetchall()

    db.commit()
    db.close()
    return msgs
def swipe(user1, user2, dirr):
    db = initdb()
    c = db.cursor()
    c.execute("SELECT * FROM swipes")
    swipes = c.fetchall()
    if dirr:
        c.execute("INSERT INTO swipes VALUES(?,?,?)", (len(swipes) + 1, user1, user2))
    else:
        c.execute("INSERT INTO swipes VALUES(?,?,?)", (-1 * (len(swipes) + 1), user1, user2))
    db.commit()
    db.close()
    return True
def getswipes(user):
    db = initdb()
    c = db.cursor()
    c.execute("SELECT * FROM swipes WHERE user1 = ?;", (user,))
    swipes = c.fetchall()
    db.close()
    return swipes
def getallswipes():
    db = initdb()
    c = db.cursor()
    c.execute("SELECT * FROM swipes;")
    swipes = c.fetchall()
    db.close()
    return swipes
def getuserid(user):
    db = initdb()
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ?;", (user,))
    uid = c.fetchone()
    db.close()
    return uid
