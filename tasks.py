"""
0. To run file type `python tasks.py in_1000000.json`.
   Example structure of `in_xxxxx.json`:
   ```
   {
    "items": [
        {
            "package": "FLEXIBLE",
            "created": "2020-03-10T00:00:00",
            "summary": [
                {
                    "period": "2019-12",
                    "documents": {
                        "incomes": 63,
                        "expenses": 13
                    }
                },
                {
                    "period": "2020-02",
                    "documents": {
                        "incomes": 45,
                        "expenses": 81
                    }
                }
            ]
        },
        {
            "package": "ENTERPRISE",
            "created": "2020-03-19T00:00:00",
            "summary": [
                {
                    "period": "2020-01",
                    "documents": {
                        "incomes": 15,
                        "expenses": 52
                    }
                },
                {
                    "period": "2020-02",
                    "documents": {
                        "incomes": 76,
                        "expenses": 47
                    }
                }
            ]
        }
    ]
   }
   ```
1. Please make below tasks described in docstring of functions in 7 days.
2. Changes out of functions body are not allowed.
3. Additional imports are not allowed.
4. Send us your solution (only tasks.py) through link in email.
   In annotations write how much time you spent for each function.
5. The data in the file is normalized.
6. Skip additional functionalities not described directly (like sorting).
7. First we will run automatic tests checking (using: 1 mln and 100 mln items):
   a) proper results and edge cases
   b) CPU usage
   c) memory usage
8. If your solution will NOT pass automatic tests (we allow some errors)
   application will be automatically rejected without additional feedback.
   You can apply again after 90 days.
9. Our develepers will review code (structure, clarity, logic).
"""
import datetime
import collections
import itertools


def task_1(data_in):
    """
    Return number of items per created[year-month].
    Add missing [year-month] with 0 if no items in data.
    ex. {
        '2020-03': 29,
        '2020-04': 0, # created[year-month] does not occur in data
        '2020-05': 24
    }
    """
    month_day_dict = collections.defaultdict(
        int
    )  # creation of a dict with default 0 value
    group_by = lambda x: x["created"][:7]
    for key, group in itertools.groupby(  # grouping objects by year,month
        sorted(
            data_in["items"], key=group_by
        ),  # need to sort by the same key function before applying groupby()
        key=group_by,
    ):
        print(key)
        month_day_dict[key] += len(list(group))  # counting objects in the group

    date_range = {
        "start_date": min(month_day_dict.keys()),
        "end_date": max(month_day_dict.keys()),
    }  # definition of the date range available in the payload

    date_objects = [
        f"{year}-{str(month).zfill(2)}"
        for year, month in itertools.product(
            range(
                int(date_range["start_date"][:4]), int(date_range["end_date"][:4]) + 1
            ),
            range(1, 13),
        )
    ]  # all the combinations of year and month available in date format

    [
        month_day_dict[y]
        for y in date_objects
        if y not in month_day_dict
        and date_range["start_date"] < y < date_range["end_date"]
    ]  # adding 0 where [year-month] does not occur in data

    return month_day_dict


def task_2(data_in):
    """
    Return number of documents per period (incomes, expenses, total).
    Return only periods provided in data.
    ex. {
        '2020-04': {
            'incomes': 2480,
            'expenses': 2695,
            'total': 5175
        },
        '2020-05': {
            'incomes': 2673,
            'expenses': 2280,
            'total': 4953
        }
    }
    """
    month_day_dict = collections.defaultdict(
        dict
    )  # creation of a dict with default {} value
    group_by = lambda x: x["period"]
    for key, group in itertools.groupby(  # grouping objects by period
        sorted(
            [
                x
                for sublist in [y["summary"] for y in data_in["items"]]
                for x in sublist
            ],  # need to sort by the same key function before applying groupby()
            key=group_by,
        ),
        key=group_by,
    ):
        objects_in_group = list(group)
        incomes_and_expenses = {
            "incomes": sum([x["documents"]["incomes"] for x in objects_in_group]),
            "expenses": sum([x["documents"]["expenses"] for x in objects_in_group]),
        }
        month_day_dict[key].update(
            {
                **incomes_and_expenses,
                "total": incomes_and_expenses["expenses"]
                + incomes_and_expenses["incomes"],
            }
        )

    return month_day_dict


def task_3(data_in):
    """
    Return arithmetic average(integer) number of documents per day
    in last three months counted from last period in data (all packages)
    for package in ['ENTERPRISE', 'FLEXIBLE']
    as one int
    ex. 64
    """
    return None


if __name__ == "__main__":
    import json
    import sys

    try:
        with open(sys.argv[1]) as fp:
            data_in = json.load(fp)
    except IndexError:
        print(
            f"""USAGE:
    {sys.executable} {sys.argv[0]} <filename>

Example:
    {sys.executable} {sys.argv[0]} in_1000000.json
"""
        )
    else:
        for func in [task_1, task_2]:  # , task_2, task_3
            print(f"\n>>> {func.__name__.upper()}")
            print(json.dumps(func(data_in), ensure_ascii=False, indent=2))
