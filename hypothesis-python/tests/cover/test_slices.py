# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2019 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import absolute_import, division, print_function

import pytest

from hypothesis import given, settings, strategies as st
from tests.common.debug import assert_all_examples, find_any, minimal

use_several_sizes = pytest.mark.parametrize("size", [1, 2, 5, 10, 100, 1000])


@use_several_sizes
def test_stop_stays_within_bounds(size):
    assert_all_examples(
        st.slices(size), lambda x: x.stop is None or (x.stop >= 0 and x.stop <= size)
    )


@use_several_sizes
def test_start_stay_within_bounds(size):
    assert_all_examples(
        st.slices(size), lambda x: x.start is None or (x.start >= 0 and x.start <= size)
    )


@use_several_sizes
def test_step_stays_within_bounds(size):
    # indices -> (start, stop, step)
    # Stop is exclusive so we use -1 as the floor.
    # This uses the indices that slice produces to make this test more readable
    # due to how splice processes None being a little complex
    assert_all_examples(
        st.slices(size),
        lambda x: (
            x.indices(size)[0] + x.indices(size)[2] <= size
            and x.indices(size)[0] + x.indices(size)[2] >= -1
        )
        or x.start == x.stop,
    )


@use_several_sizes
def test_step_will_not_be_zero(size):
    assert_all_examples(st.slices(size), lambda x: x.step != 0)


@use_several_sizes
def test_slices_will_shrink(size):
    sliced = minimal(st.slices(size))
    assert sliced.start == 0 or sliced.start is None
    assert sliced.stop == 0 or sliced.stop is None
    assert sliced.step == 1


@given(st.integers(1, 1000))
@settings(deadline=None)
def test_step_will_be_negative(size):
    find_any(st.slices(size), lambda x: x.step < 0)


@given(st.integers(1, 1000))
@settings(deadline=None)
def test_step_will_be_positive(size):
    find_any(st.slices(size), lambda x: x.step > 0)


@given(st.integers(1, 10))
@settings(deadline=None)
def test_stop_will_equal_size(size):
    find_any(st.slices(size), lambda x: x.stop == size)


@given(st.integers(1, 10))
@settings(deadline=None)
def test_start_will_equal_size(size):
    find_any(st.slices(size), lambda x: x.start == size - 1)


@given(st.integers(1, 1000))
@settings(deadline=None)
def test_start_will_equal_0(size):
    find_any(st.slices(size), lambda x: x.start == 0)


@given(st.integers(1, 1000))
@settings(deadline=None)
def test_start_will_equal_stop(size):
    find_any(st.slices(size), lambda x: x.start == x.stop)
