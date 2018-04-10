import auth

db_right = list()
db_right.append(('daniel', 'vargas', '=2od%]1*9Q', 9966))
db_right.append(('nadine', 'heere', 'j=U]V.n`l\\', 10976))
db_right.append(('mayar', 'ali', 'PJM0~RD*|&', 6986))
db_right.append(('marc', 'vischer', 'nL*E~T&az1', 13112))
db_right.append(('pooja', 'subramaniam', '%9<:%fSN$}', 18453))

db_wrong = list()
db_wrong.append(('joel', 'afreth', 'c:d{<Am),Z', 11060)) # should be 11069

db_dict_right = dict()
for user in db_right:
    db_dict_right[user[0]] = (user[3], user[2])

db_dict_wrong = dict()
for user in db_wrong:
    db_dict_wrong[user[0]] = (user[3], user[2])

def test_get_salt():
    salts = [auth.get_salt() for i in range(100)]
    assert all([len(salt) == 10 for salt in salts]), 'Some are not 10 characters long'
    assert len(set(salts)) == len(salts), 'Tested 100 salts are not unique'


def test_pwhash():
    for user in db_right:
        assert auth.pwhash(user[1], user[2]) == user[3]

    for user in db_wrong:
        assert auth.pwhash(user[1], user[2]) != user[3]


def test_authenticate():
    for user in db_right:
        assert auth.authenticate(user[0], user[1], db_dict_right)

    for user in db_wrong:
        assert not auth.authenticate(user[0], user[1], db_dict_wrong)
