import datetime
import numpy
import os
import unittest
import pydst


class TestGetValues(unittest.TestCase):
    """Test the `get_values` function."""
    def setUp(self):
        self.data = os.path.join(os.path.dirname(__file__), 'data')

    def test_non_existent(self):
        """Test with non existent file."""
        self.assertRaises(IOError, pydst.get_values, "xxx")

    def test_less_than_120(self):
        """First line shorter than 120 chars."""
        testfile = os.path.join(self.data, "dst_wrong_lines.txt")
        self.assertRaises(ValueError, pydst.get_values, testfile)

    def test_missing_dst_prefix(self):
        """Prefix != 'DST'."""
        testfile = os.path.join(self.data, "dst_missing_prefix.txt")
        self.assertRaises(ValueError, pydst.get_values, testfile)

    def test_wrong_date(self):
        """Test with a wrong date."""
        testfile = os.path.join(self.data, "dst_wrong_date.txt")
        self.assertRaises(ValueError, pydst.get_values, testfile)

    def test_wrong_value(self):
        """Test with a wrong value."""
        testfile = os.path.join(self.data, "dst_wrong_value.txt")
        self.assertRaises(ValueError, pydst.get_values, testfile)

    def test_no_dates(self):
        """Test without start/end dates."""
        testfile = os.path.join(
            self.data,
            'SW_OPER_AUX_DST_2F_20160720T000000_20160722T055959_0001.DBL'
        )
        r_t = numpy.array([datetime.datetime(2016, 7, 20, 1, 0),
                           datetime.datetime(2016, 7, 20, 2, 0),
                           datetime.datetime(2016, 7, 20, 3, 0),
                           datetime.datetime(2016, 7, 20, 4, 0),
                           datetime.datetime(2016, 7, 20, 5, 0),
                           datetime.datetime(2016, 7, 20, 6, 0),
                           datetime.datetime(2016, 7, 20, 7, 0),
                           datetime.datetime(2016, 7, 20, 8, 0),
                           datetime.datetime(2016, 7, 20, 9, 0),
                           datetime.datetime(2016, 7, 20, 10, 0),
                           datetime.datetime(2016, 7, 20, 11, 0),
                           datetime.datetime(2016, 7, 20, 12, 0),
                           datetime.datetime(2016, 7, 20, 13, 0),
                           datetime.datetime(2016, 7, 20, 14, 0),
                           datetime.datetime(2016, 7, 20, 15, 0),
                           datetime.datetime(2016, 7, 20, 16, 0),
                           datetime.datetime(2016, 7, 20, 17, 0),
                           datetime.datetime(2016, 7, 20, 18, 0),
                           datetime.datetime(2016, 7, 20, 19, 0),
                           datetime.datetime(2016, 7, 20, 20, 0),
                           datetime.datetime(2016, 7, 20, 21, 0),
                           datetime.datetime(2016, 7, 20, 22, 0),
                           datetime.datetime(2016, 7, 20, 23, 0),
                           datetime.datetime(2016, 7, 21, 0, 0),
                           datetime.datetime(2016, 7, 21, 1, 0),
                           datetime.datetime(2016, 7, 21, 2, 0),
                           datetime.datetime(2016, 7, 21, 3, 0),
                           datetime.datetime(2016, 7, 21, 4, 0),
                           datetime.datetime(2016, 7, 21, 5, 0),
                           datetime.datetime(2016, 7, 21, 6, 0),
                           datetime.datetime(2016, 7, 21, 7, 0),
                           datetime.datetime(2016, 7, 21, 8, 0),
                           datetime.datetime(2016, 7, 21, 9, 0),
                           datetime.datetime(2016, 7, 21, 10, 0),
                           datetime.datetime(2016, 7, 21, 11, 0),
                           datetime.datetime(2016, 7, 21, 12, 0),
                           datetime.datetime(2016, 7, 21, 13, 0),
                           datetime.datetime(2016, 7, 21, 14, 0),
                           datetime.datetime(2016, 7, 21, 15, 0),
                           datetime.datetime(2016, 7, 21, 16, 0),
                           datetime.datetime(2016, 7, 21, 17, 0),
                           datetime.datetime(2016, 7, 21, 18, 0),
                           datetime.datetime(2016, 7, 21, 19, 0),
                           datetime.datetime(2016, 7, 21, 20, 0),
                           datetime.datetime(2016, 7, 21, 21, 0),
                           datetime.datetime(2016, 7, 21, 22, 0),
                           datetime.datetime(2016, 7, 21, 23, 0),
                           datetime.datetime(2016, 7, 22, 0, 0),
                           datetime.datetime(2016, 7, 22, 1, 0),
                           datetime.datetime(2016, 7, 22, 2, 0),
                           datetime.datetime(2016, 7, 22, 3, 0),
                           datetime.datetime(2016, 7, 22, 4, 0),
                           datetime.datetime(2016, 7, 22, 5, 0),
                           datetime.datetime(2016, 7, 22, 6, 0)], dtype=datetime.datetime)
        r_dst = numpy.array([43, 27, 13, -2, -18, -23, -26, -24, -16, -12, -5, 1,
                             10, 10, 8, 1, -3, -6, -12, -12, -10, -12, -13, -14,
                             -13, -8, -10, -8, -5, -5, -8, -9, -7, -10, -10, -8,
                             -7, -6, -11, -6, -4, -6, -8, -10, -9, -10, -9, -12,
                             -10, -6, -4, -1, -2, -8])
        result = pydst.get_values(testfile)
        self.assertIsInstance(result, dict)
        self.assertEqual(['timestamp', 'dst'], list(result.keys()))
        self.assertIsInstance(result['timestamp'], numpy.ndarray)
        numpy.testing.assert_array_equal(result['timestamp'], r_t)
        self.assertIsInstance(result['dst'], numpy.ndarray)
        numpy.testing.assert_array_equal(result['dst'], r_dst)

    def test_with_dates(self):
        """Test with time filter:
        2016-07-20 04:00:00 <= t <= 2016-07-20 14:00:00.
        """
        testfile = os.path.join(
            self.data,
            'SW_OPER_AUX_DST_2F_20160720T000000_20160722T055959_0001.DBL'
        )
        r_t = numpy.array([datetime.datetime(2016, 7, 20, 4, 0),
                           datetime.datetime(2016, 7, 20, 5, 0),
                           datetime.datetime(2016, 7, 20, 6, 0),
                           datetime.datetime(2016, 7, 20, 7, 0),
                           datetime.datetime(2016, 7, 20, 8, 0),
                           datetime.datetime(2016, 7, 20, 9, 0),
                           datetime.datetime(2016, 7, 20, 10, 0),
                           datetime.datetime(2016, 7, 20, 11, 0),
                           datetime.datetime(2016, 7, 20, 12, 0),
                           datetime.datetime(2016, 7, 20, 13, 0),
                           datetime.datetime(2016, 7, 20, 14, 0)], dtype=datetime.datetime)
        r_dst = numpy.array([-2, -18, -23, -26, -24, -16, -12, -5, 1,
                             10, 10])
        result = pydst.get_values(
            testfile,
            begin_date=datetime.datetime(2016, 7, 20, 4, 0),
            end_date=datetime.datetime(2016, 7, 20, 14, 0)
        )
        self.assertIsInstance(result['timestamp'], numpy.ndarray)
        numpy.testing.assert_array_equal(result['timestamp'], r_t)
        self.assertIsInstance(result['dst'], numpy.ndarray)
        numpy.testing.assert_array_equal(result['dst'], r_dst)


if __name__ == '__main__':
    unittest.main()
