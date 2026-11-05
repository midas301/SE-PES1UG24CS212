import pytest
from train_fare import base_fare, concession, tatkal_charge

# base_fare
def test_sleeper_fare():
    assert base_fare("SL", 500) == 500

def test_unknown_class():
    with pytest.raises(ValueError):
        base_fare("XX", 100)

def test_invalid_distance():
    with pytest.raises(ValueError):
        base_fare("SL", 0)

def test_minimum_fare():
    assert base_fare("SL", 10) == 50

# concession
def test_adult_no_concession():
    assert concession(30, "M", False) == 0

def test_tatkal_no_concession():
    assert concession(70, "F", True) == 0

def test_infant():
    assert concession(3, "M", False) == 100

def test_child():
    assert concession(10, "F", False) == 50

def test_senior_male():
    assert concession(65, "M", False) == 40

def test_senior_female():
    assert concession(65, "F", False) == 50

# tatkal_charge
def test_tatkal_sl_min():
    assert tatkal_charge("SL", 500) == 100

def test_tatkal_non_sl_max():
    assert tatkal_charge("3A", 2000) == 400
