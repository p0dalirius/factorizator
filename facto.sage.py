#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : facto.sage.py
# Author             : Podalirius (@podalirius_)
# Date created       : 14 May 2022


import argparse
import json
import requests
import time


factordb_status = {
    'C': 'Composite, no factors known',
    'CF': 'Composite, factors known',
    'FF': 'Composite, fully factored',
    'P': 'Definitely prime',
    'Prp': 'Probably prime',
    'U': 'Unknown',
    'Unit': 'Just for "1"',
    'N': 'Number is not in database (and was not added due to your settings)',
    '*': 'Number added to database during this request'
}


def delta_time(delta_t, units=["hours", "minutes", "seconds", "miliseconds"]):
    out = ""
    if delta_t // 3600 != 0:  # hours
        out = out + str(int(delta_t // 3600)) + " " + units[0]
        delta_t = delta_t % 3600
    if delta_t // 60 != 0:  # minutes
        out = out + " " + str(int(delta_t // 60)) + " " + units[1]
        delta_t = delta_t % 60
    if int(delta_t) != 0:  # seconds
        out = out + " " + str(int(delta_t)) + " " + units[2]
        delta_t = delta_t - int(delta_t)
    if delta_t // 0.001 != 0:  # miliseconds
        out = out + " " + str(int(delta_t // 0.001)) + " " + units[3]
    if out == "":
        out = "0 " + units[-1]
    out = out + "."
    if out.startswith(" "):
        out = out[1:]
    return out


def try_factordb(number):
    # Searching on FactorDB ====================================================
    factors = []
    try:
        from factordb.factordb import FactorDB
    except ImportError as e:
        print("pip install factordb-pycli")
    else:
        print("\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Searching on FactorDB ... ", end="")
        try:
            f = FactorDB(number)
            f.connect()
            factors = f.get_factor_list()  # weird when not FF
        except requests.exceptions.ConnectionError as e:
            print("\x1b[1;91mCould not reach FactorDB.\x1b[0m")
            return None

    # Factors found on FactorDB ================================================
    if len(factors) != 0:
        print("\x1b[1;92mFound on FactorDB !\x1b[0m")
        if f.get_status() == 'FF':
            print("\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Factors :\n")
            counted_factors = [[f, factors.count(f)] for f in set(factors)]
            print(' * '.join([str(f) + "^" + str(occ) if occ != 1 else str(f) for (f, occ) in counted_factors]))
            writefactors(number, counted_factors)
            return True
        elif f.get_status() == 'P':
            print("\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Given number is a prime number.\n")
            counted_factors = [[f, factors.count(f)] for f in set(factors)]
            print(' * '.join([str(f) + "^" + str(occ) if occ != 1 else str(f) for (f, occ) in counted_factors]))
            writefactors(number, counted_factors)
            return True
        else:
            print("\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Status : %s %s\n" % (f.get_status(), factordb_status[f.get_status()]))
            return False
    else:
        print("\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m No factors known on FactorDB.\n")
        return False


def try_facto_sage(number):
    """Documentation for try_sage"""
    # Not found, starting SageMath =============================================
    starting_time = time.time()
    print("\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Factoring N ... ", end="")
    factors = factor(number)
    stopping_time = time.time()
    print("        \x1b[1m\x1b[92mDone.\x1b[0m")
    print(
        "\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Factoring time : %s"
        % delta_time(stopping_time - starting_time)
    )
    print("\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Factors :\n")
    print(factors)
    writefactors(number, factors)
    return


def writefactors(number, factors, filename='factors.json'):
    print("\n\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Writing %s file ..." % filename)
    f = open(filename, 'w')
    f.write(json.dumps({'number': number, 'factors': [[int(tmp[0]), int(tmp[1])] for tmp in list(factors)]}, indent=4))
    f.write("\n")
    f.close()
    print("\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Done.")


banner = r"""  _____          _             _          _
 |  ___|_ _  ___| |_ ___  _ __(_)______ _| |_ ___  _ __
 | |_ / _` |/ __| __/ _ \| '__| |_  / _` | __/ _ \| '__|  v1.3
 |  _| (_| | (__| || (_) | |  | |/ / (_| | || (_) | |
 |_|  \__,_|\___|\__\___/|_|  |_/___\__,_|\__\___/|_|     by Remi GASCOU (Podalirius)

"""

if __name__ == '__main__':
    print(banner)
    parser = argparse.ArgumentParser(description='Factorize an integer.')
    parser.add_argument('-n', '--number', required=True, help='Integer to factorize.')
    args = parser.parse_args()

    if args.number.startswith('0x'):
        number = int(args.number[2:], 16)
    else:
        number = int(args.number)

    found = try_factordb(number)
    if not found:
        print("\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Loading sage library ... ", end="")
        try:
            from sage.all import *
        except ImportError as e:
            print("\n\x1b[1m[\x1b[91mWARN\x1b[0m\x1b[1m]\x1b[0m SageMath is not installed.")
            print("       Install it with : sudo apt install sagemath")
        else:
            print("\x1b[1m\x1b[92mDone.\x1b[0m")
            try_facto_sage(number)
