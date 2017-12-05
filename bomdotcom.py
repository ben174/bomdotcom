#!/usr/bin/env python
import json
import logging
import re
from sets import Set

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)


aggregates = {}
formats = [
    r'(?P<mpn>.*):(?P<manufacturer>.*):(?P<refdegs>.*)',
    r'(?P<manufacturer>.*) -- (?P<mpn>.*):(?P<refdegs>.*)',
    r'(?P<refdegs>.*);(?P<mpn>.*);(?P<manufacturer>.*)',
]


def extract_row(row):
    '''
    Input: A string in one of three formats:
        MPN:Manufacturuer:ReferenceDesignators
        Manufacturer -- MPN:ReferenceDesignators
        ReferenceDesignators;MPN;Manufacturer

    Output: A dictionary with keys: manufacturer, mpn, refdegs

    NOTE: It's entirely possible a bad row of data could 'fool'
    this method by having a funky Manufacturuer name containing
    semicolons or other data constructed specificaly to break this.
    I'm not accounting for this in this extraction method, and will
    assume all input data is sane, based on example input provided
    in the spec.

    If I couldn't trust the integrity of the input data, I would
    move data validation/sanitation to another tool which would run
    earlier in on the pipeline.

    '''
    # these formats differ enough where I can assume the first match wins
    for f in formats:
        logging.debug('Searching {}, against regex: {}'.format(row, f))
        result = re.search(f, row)
        if result:
            result = result.groupdict()
            result['refdegs'] = result['refdegs'].split(',')
            return result
    raise ValueError('Malformed data row: {}'.format(row))


def process_row(line):
    row = extract_row(line)
    key = (row['mpn'], row['manufacturer'])
    if key not in aggregates:
        aggregates[key] = {'count': 1, 'refdegs': Set(row['refdegs'])}
    else:
        aggregates[key]['count'] += 1
        aggregates[key]['refdegs'].update(row['refdegs'])
    logging.debug('Row: {} -> {}: {}'.format(row, str(key), aggregates[key]))


def format_aggregates():
    ret = []
    for (mpn, manufacturer), value in aggregates.items():
        ret.append({
            'MPN': mpn,
            'Manufacturer': manufacturer,
            'ReferenceDesignators': sorted(list(value['refdegs'])),
            'NumOccurrences': value['count'],
        })
    # sort by refdeg count, then by occurrence count
    ret = sorted(ret, key=lambda k: len(k['ReferenceDesignators']), reverse=True)
    ret = sorted(ret, key=lambda k: k['NumOccurrences'], reverse=True)
    return ret


def main():
    output_count = 1
    try:
        output_count = int(raw_input())
        while True:
            process_row(raw_input())
    except EOFError:
        pass
    formatted = format_aggregates()
    print json.dumps(formatted[:output_count])


if __name__ == '__main__':
    main()
