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

# --- extra tests for branch coverage ---
def test_tatkal_sl_in_range():
    assert tatkal_charge("SL", 2000) == 200

def test_tatkal_non_sl_in_range():
    assert tatkal_charge("3A", 1000) == 300

def test_tatkal_exactly_100():
    assert tatkal_charge("SL", 1000) == 100

def test_tatkal_exactly_400():
    assert tatkal_charge("1A", 1334) == 400

def test_tatkal_sl_above_cap():
    assert tatkal_charge("SL", 5000) == 400

def test_distance_negative():
    with pytest.raises(ValueError):
        base_fare("2A", -5)

def test_fare_exactly_50():
    assert base_fare("SL", 50) == 50

def test_fare_above_min_non_sl():
    assert base_fare("1A", 100) == 500

def test_age_4_and_5():
    assert concession(4, "M", False) == 100
    assert concession(5, "M", False) == 50

def test_age_12_and_13():
    assert concession(12, "F", False) == 50
    assert concession(13, "F", False) == 0

def test_age_59_and_60():
    assert concession(59, "M", False) == 0
    assert concession(60, "M", False) == 40

def test_tatkal_child_no_concession():
    assert concession(8, "M", True) == 0
