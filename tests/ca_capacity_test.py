# Copyright 2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from typing import Optional
from grscheller.circular_array.ca import CA

class TestCapacity:

    def test_capacity_original(self) -> None:
        c: CA[int] = CA()
        assert c.capacity() == 2

        c = CA(1, 2)
        assert c.fractionFilled() == 2/4

        c.push_front(0)
        assert c.fractionFilled() == 3/4

        c.push_rear(3)
        assert c.fractionFilled() == 4/4

        c.push_rear(4)
        assert c.fractionFilled() == 5/8

        c.push_front(5)
        assert c.fractionFilled() == 6/8

        assert len(c) == 6
        assert c.capacity() == 8

        c.resize()
        assert c.fractionFilled() == 6/8

        c.resize(30)
        assert c.fractionFilled() == 6/30

        c.resize(3)
        assert c.fractionFilled() == 6/8

        c.pop_front_unsafe()
        c.pop_rear_unsafe()
        c.pop_front_unsafe()
        c.pop_rear_unsafe()
        assert c.fractionFilled() == 2/8
        c.resize(3)
        assert c.fractionFilled() == 2/4
        c.resize(7)
        assert c.fractionFilled() == 2/7


    def test_double(self) -> None:
        c: CA[int] = CA(1, 2, 3)
        assert c.pop_front_unsafe() == 1
        assert c.capacity() == 5
        c.double()
        assert c.capacity() == 10
        c.double()
        c.push_front(666)
        c.push_rear(0)
        assert len(c) == 4
        assert c.capacity() == 20
        c.resize()
        assert c.capacity() == 6
        c.push_front(2000)
        assert len(c) == 5
        assert c.capacity() == 6
        for ii in range(45):
            if ii % 3 == 0:
                c.push_rear(c.pop_front_unsafe())
                c.push_front(ii+100)
            else:
                c.push_rear(ii+1000)
        assert len(c) == 50
        assert c.capacity() == 96
        jj = len(c)
        assert jj == 50
        while jj > 0:
            kk = c.pop_front_unsafe()
            assert kk != -1
            c.push_rear(kk)
            jj -= 1
        assert len(c) == 50
        assert c.fractionFilled() == 50/96
        assert c.capacity() == 96
        c.compact()
        assert c.capacity() == 52

    def test_empty(self) -> None:
        c: CA[int] = CA()
        assert c == CA()
        assert c.capacity() == 2
        c.double()
        assert c.capacity() == 4
        c.compact()
        assert c.capacity() == 2
        c.resize(6)
        assert c.capacity() == 6
        assert len(c) == 0

    def test_one(self) -> None:
        c = CA(42)
        assert c.capacity() == 3
        c.compact()
        assert c.capacity() == 3
        c.resize(8)
        assert c.capacity() == 8
        assert len(c) == 1
        popped = c.pop_front_unsafe()
        assert popped == 42
        assert len(c) == 0
        assert c.capacity() == 8
        try:
            c.pop_front_unsafe()
        except ValueError as ve:
            str(ve) == 'foofoo'
        else:
            assert False
        try:
            c.pop_rear_unsafe()
        except ValueError as ve:
            str(ve) == 'foofoo'
        else:
            assert False
        c.push_rear(popped)
        assert len(c) == 1
        assert c.capacity() == 8
        c.resize(5)
        assert c.capacity() == 5
        assert len(c) == 1
        c.resize()
        assert c.capacity() == 3
