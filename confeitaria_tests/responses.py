#!/usr/bin/env python
#
# Copyright 2015 Adam Victor Brandizzi
#
# This file is part of Confeitaria.
#
# Confeitaria is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Confeitaria is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Confeitaria.  If not, see <http://www.gnu.org/licenses/>.
import unittest

import inelegant.finder

from confeitaria import responses


class TestResponses(unittest.TestCase):

    def test_receive_message_as_first_argument(self):
        """
        A response should receive the message to go into the response as the
        first argument
        """
        response = responses.NotFound('my message')
        self.assertEquals('my message', response.message)


load_tests = inelegant.finder.TestFinder(__name__, responses).load_tests

if __name__ == "__main__":
    unittest.main()
