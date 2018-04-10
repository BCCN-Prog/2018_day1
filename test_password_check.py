#test_pass.py

import password_check as pw
import getpass
import pathlib
import pickle
import random
import string
import tempfile

PWDB_FLNAME = pathlib.Path('pwdb.pkl')
CHARS = string.ascii_letters + string.digits + string.punctuation

def test_get_credentials():
    testusername = 'bob'
    testpassword = 'frog'
    username, password = pw.get_credentials()
    assert testusername == username
    assert testpassword == password
