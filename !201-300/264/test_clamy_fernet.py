from datetime import datetime
from random import choice
from tempfile import NamedTemporaryFile

import pytest
from clamy_fernet import PBKDF2HMAC, ByteString, ClamyFernet, Fernet

KEYS = (
    b"rvxePMSDUcZFowEaNxnFb8Pifn1KmhkF70Mz1ZQe2Bw=",
    b"2gODW4C4Lc7H9bjuuhPyn48HkVHriqa96P8lmstABo8=",
    b"mAbAfF5CW3EGlngOEEroDqtxlxVlJILzoUE4TJScMIw=",
)
MESSAGE = "This is my secret message"
TMP_FILE = NamedTemporaryFile(delete=False)
FILE = TMP_FILE.name


@pytest.fixture(scope="function")
def rcf():
    password = b"#clamybite"
    key = choice(KEYS)
    return ClamyFernet(password, key)


@pytest.fixture(scope="module")
def cf():
    return ClamyFernet(key=KEYS[0])


def test_clamyfernet_no_args(rcf):
    tmp_cf = ClamyFernet()
    assert tmp_cf.key is not None
    assert tmp_cf.password == b"pybites"


def test_clamyfernet_random_key(rcf):
    token = rcf.encrypt("secret msg")
    ts = rcf.clf.extract_timestamp(token)
    dt = datetime.fromtimestamp(ts)
    assert isinstance(rcf, ClamyFernet)
    assert isinstance(rcf.clf, Fernet)
    assert isinstance(rcf.key, ByteString)
    assert isinstance(rcf.kdf, PBKDF2HMAC)
    assert dt.year == datetime.now().year


def test_clamyfernet(cf):
    token = cf.encrypt(MESSAGE)
    og_message = cf.decrypt(token)
    assert len(token) == 120
    assert isinstance(token, bytes)
    assert cf.key == KEYS[0]
    assert og_message == MESSAGE


def test_clamyfernet_random(rcf):
    token = rcf.encrypt(MESSAGE)
    og_message = rcf.decrypt(token)
    assert len(token) == 120
    assert isinstance(token, bytes)
    assert rcf.key in KEYS
    assert og_message == MESSAGE
