from datetime import datetime


def sort_by_date(raw_tasks):
    sorted_tasks = raw_tasks
    for i in range(len(raw_tasks)):
        key = raw_tasks[i]
        j = i - 1;
        while j >= 0 and not comp_dates(raw_tasks[j]["timestamp"], key["timestamp"]):
            raw_tasks[j + 1] = raw_tasks[j]
            j = j - 1
        raw_tasks[j + 1] = key

    return sorted_tasks


def comp_dates(t1, t2):
    pt1 = parse_datetime(t1)
    pt2 = parse_datetime(t2)

    return (pt1 < pt2)


def parse_datetime(timestamp):
    date_format = "%a, %d %b %Y %H:%M:%S %Z"

    parsed_date = datetime.strptime(timestamp, date_format)
    return parsed_date


