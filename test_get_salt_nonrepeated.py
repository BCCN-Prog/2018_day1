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

def test_get_salt_nonrepeated():
    salts=[]
    for i in range(20):
        salts.append(pw.get_salt())
    for i,salt in enumerate(salts):
        for j,others in enumerate(salts):
            if i == j:
                assert (salt==others)
            elif i != j:
                assert (salt!=others)
