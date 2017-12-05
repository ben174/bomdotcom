#!/usr/bin/env python
import logging
import unittest

from bomdotcom import extract_row, process_row


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


test_data = {
    'TSR-1002:Panasonic:A1,D2': {'mpn': 'TSR-1002', 'refdegs': ['A1', 'D2'], 'manufacturer': 'Panasonic'},
    'Panasonic -- TSR-1002:A1': {'mpn': 'TSR-1002', 'refdegs': ['A1'], 'manufacturer': 'Panasonic'},
    'A1,B2,C8;TSR-1002;Keystone': {'mpn': 'TSR-1002', 'refdegs': ['A1', 'B2', 'C8'], 'manufacturer': 'Keystone'},
}


class TestBomDotCom(unittest.TestCase):
    def test_extract_row(self):
        for key, value in test_data.items():
            self.assertEqual(extract_row(key), value)

    def test_extract_invalid_row(self):
        with self.assertRaises(ValueError) as context:
            extract_row('xxx')
            self.assertTrue('xxx' in context.exception)


if __name__ == '__main__':
    unittest.main()
