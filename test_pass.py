import login
import random
import string
CHARS = string.ascii_letters + string.digits + string.punctuation

def get_rand_string():
    salt_chars = random.choices(CHARS, k=10)
    return ''.join(salt_chars)

def test_getsalt_type():
    assert type(login.get_salt())==type('sillystring')

def test_auth_user_known_pw_correct():
    user = 'normalusername'
    password = 'r34s0n4bl3_passw0rd!'
    salt = login.get_salt()
    hash = login.pwhash(password,salt)
    pwdb = {user:(hash,salt)}
    assert login.authenticate(user,password,pwdb) is True
    for i in range(10):
        u = get_rand_string()
        p = get_rand_string()
        salt = login.get_salt()
        hash = login.pwhash(p,salt)
        pwdb = {u:(hash,salt)}
        assert login.authenticate(u,p,pwdb) is True

def test_auth_user_known_pw_wrong():
    user = 'normalusername'
    password = 'r34s0n4bl3_passw0rd!'
    wrongpassword = 'r34s0n4ble_p4ssw0rd!'
    salt = login.get_salt()
    hash = login.pwhash(wrongpassword,salt)
    pwdb = {user:(hash,salt)}
    assert login.authenticate(user,password,pwdb) is False
    for i in range(10):
        u = get_rand_string()
        p = get_rand_string()
        wp = get_rand_string()
        salt = login.get_salt()
        hash = login.pwhash(wp,salt)
        pwdb = {u:(hash,salt)}
        assert login.authenticate(u,p,pwdb) is False

def test_auth_user_unkown():
    wronguser = 'wrongusername'
    user = 'normalusername'
    password = 'r34s0n4bl3_passw0rd!'
    salt = login.get_salt()
    hash = login.pwhash(password,salt)
    pwdb = {user:(hash,salt)}
    assert login.authenticate(wronguser,password,pwdb) is False
    for i in range(10):
        u = get_rand_string()
        wu = get_rand_string()
        p = get_rand_string()
        salt = login.get_salt()
        hash = login.pwhash(p,salt)
        pwdb = {u:(hash,salt)}
        assert login.authenticate(wu,p,pwdb) is False

def test_read_pwdb_nofile():
    filename = '/tmp/nodatabase.pkl'
    assert login.read_pwdb(filename) == {}

def test_pwhash_repeatable():
    for i in range(100):
        p = get_rand_string()
        s = login.get_salt()
        h1 = login.pwhash(p,s)
        h2 = login.pwhash(p,s)
        assert h1 == h2

def test_add_user_newuser():
    u = get_rand_string()
    p = get_rand_string()
    salt = get_rand_string()
    pwdb_file = './tmp/pwdb.pkl'
    pwdb = {}
    login.add_user(u,p,salt,pwdb,pwdb_file)
    hash = login.pwhash(p,salt)
    target_pwdb = {u:(hash,salt)}
    pwdb = login.read_pwdb(pwdb_file)
    assert target_pwdb == pwdb
    for i in range(10):
        u = get_rand_string()
        p = get_rand_string()
        salt = get_rand_string()
        login.add_user(u,p,salt,pwdb,pwdb_file)
        hash = login.pwhash(p,salt)
        target_pwdb[u] = (hash,salt)
        pwdb = login.read_pwdb(pwdb_file)
        assert target_pwdb == pwdb
