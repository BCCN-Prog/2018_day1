from passw import *
import random

CHARS = string.ascii_letters + string.digits + string.punctuation
PWDB_FLNAME = pathlib.Path('pwdb.pkl')
pwdb = {}
write_pwdb(pwdb, open('/tmp/pwdb.pkl', 'wb'))

def test_salt():
    salts = [get_salt() for i in range(121)]
    assert len(set(salts)) > 1

def test_hash(N = 20):
    salts = [get_salt() for i in range(N)]
    passwords = [''.join(random.sample(CHARS, k = 5)) for i in range(N)]
    hashes = [pwhash(p, s) for (p, s) in zip(passwords, salts)]

    print(salts)
    print(passwords)
    th = 0.9
    assert len(set(hashes)) > N * (1 - th)


def test_user_added():
    path = '/tmp/pwdb.pkl'
    pwdb_file = open(path, 'rb')
    pwdb = read_pwdb(pwdb_file)
    start = len(pwdb)
    usernames, passwords = [str(i) for i in range(10)], [str(i + 123) for i in range(10)]
    pwdb_file = open(path, 'wb')
    for uname, password in zip(usernames, passwords):
        salt = get_salt()
        add_user(uname, password, salt, pwdb, pwdb_file)
    assert len(pwdb) == start + 10

def test_can_login():
    path = '/tmp/pwdb.pkl'
    pwdb_file = open(path, 'rb')
    pwdb = read_pwdb(pwdb_file)
    username = 'Pantelis2'
    password = 'imgay2'
    salt = get_salt()
    pwdb_file = open(path, 'wb')
    add_user(username, password, salt, pwdb, pwdb_file)
    assert authenticate(username, password, pwdb)
