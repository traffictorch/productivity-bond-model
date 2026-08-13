"""Basic unit tests."""

import numpy as np
import pytest

from config import get_config
from state_generator import simulate_paths
from bond_valuation import compute_coupons, present_value_cost


@pytest.fixture
def small_cfg():
    return get_config(n_paths=200, n_years=5, seed=123)


def test_paths_shapes(small_cfg):
    paths = simulate_paths(small_cfg)
    assert paths.g_y.shape == (200, 5)
    assert paths.g_n.shape == (200, 5)
    assert paths.primary_balance.shape == (200, 5)


def test_growth_means_reasonable(small_cfg):
    paths = simulate_paths(small_cfg)
    assert 0.00 < np.mean(paths.g_y) < 0.06
    assert 0.00 < np.mean(paths.g_n) < 0.06


def test_coupon_conventional(small_cfg):
    paths = simulate_paths(small_cfg)
    c = compute_coupons(paths, "conventional", small_cfg)
    assert np.allclose(c, small_cfg.conventional_coupon)


def test_present_value_shape(small_cfg):
    paths = simulate_paths(small_cfg)
    c = compute_coupons(paths, "conventional", small_cfg)
    pv = present_value_cost(c, small_cfg)
    assert pv.shape == (200,)
    assert np.all(pv > 0)


def test_reproducibility():
    cfg1 = get_config(n_paths=100, n_years=3, seed=99)
    cfg2 = get_config(n_paths=100, n_years=3, seed=99)
    p1 = simulate_paths(cfg1)
    p2 = simulate_paths(cfg2)
    np.testing.assert_array_equal(p1.g_y, p2.g_y)
