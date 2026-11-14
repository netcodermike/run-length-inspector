from itertools import groupby

def analyze(data):
    values = data['values']
    if not isinstance(values, list) or any(type(v) is not int or not 0 <= v <= 255 for v in values):
        raise ValueError('Expected byte values')
    runs = []
    for value, group in groupby(values):
        count = sum(1 for _ in group)
        while count:
            size = min(count, 255)
            runs.append([value, size])
            count -= size
    decoded = [value for value, size in runs for _ in range(size)]
    return {'runs': runs, 'rawBytes': len(values), 'encodedBytes': 2 * len(runs), 'roundTrip': decoded == values}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
