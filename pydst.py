import datetime
import numpy
import re


__version__ = '1.2'


def get_values(filename, begin_date=None, end_date=None):
    """Extract timestamps and Dst indices from `filename`.

    Parameters
    ----------
    filename : str
        Dst indices file.
    begin_date : date, datetime or None
        get values having timestamps greater than or equal to `begin_date`.
    end_date : date, datetime or None
        get values having timestamps lower than or equal to `end_date`.

    Returns
    -------
    dict of numpy.array
        timestamps and Dst indices extracted from `filename`.

    Raises
    ------
    IOError
        if `filename` is not readable.
    TypeError
        if type of `begin_date` or `end_date` is wrong.
    ValueError
        if `filename` is not valid.
    """
    # Check filename
    if not isinstance(filename, str):
        raise TypeError('filename must be str, not %s' % type(str))

    # Check dates
    if begin_date is None:
        begin_date = datetime.datetime(datetime.MINYEAR, 1, 1)
    elif isinstance(begin_date, datetime.date):
        if isinstance(begin_date, datetime.datetime):
            pass
        else:
            begin_date = datetime.datetime.combine(begin_date, datetime.time())
    else:
        raise TypeError('begin_date must be date, datetime or None, not %s' % type(begin_date))
    if end_date is None:
        end_date = datetime.datetime(datetime.MAXYEAR, 12, 31, 23, 59, 59, 999999)
    elif isinstance(end_date, datetime.date):
        if isinstance(end_date, datetime.datetime):
            pass
        else:
            end_date = datetime.datetime.combine(end_date, datetime.time())
    else:
        raise TypeError('end_date must be date, datetime or None, not %s' % type(begin_date))

    # Fetch data
    params = {
        'timestamp': [],
        'dst': []
    }
    record = re.compile(
        r'DST(?P<y2>\d{2})(?P<month>\d{2})\*(?P<day>\d{2})([ a-zA-Z]{2})X(?P<version>(\d| ))(?P<y1>\d{2})'
        r'(?P<base>[ 0-9]{4})(?P<dst>([- 0-9]{4}){24})(?P<mean>[- 0-9]{4})'
    )
    with open(filename) as f:
        for n, line in enumerate(f, 1):
            match = record.match(line)
            if match:
                try:
                    group = match.groupdict()
                    ts = datetime.datetime(
                        int(group['y1'] + group['y2']),
                        int(group['month']),
                        int(group['day'])
                    )
                    for i in range(0, 24):
                        value = int(group['dst'][i * 4: i * 4 + 4])
                        if value != 9999:
                            ts += datetime.timedelta(hours=1)
                            if begin_date <= ts <= end_date:
                                params['timestamp'].append(ts)
                                params['dst'].append(value)
                        else:
                            break
                except ValueError:
                    raise ValueError('line %d not valid' % n)
            else:
                raise ValueError('line %d not valid' % n)

    # convert lists to arrays and return values
    return {p: numpy.array(params[p]) for p in params}
