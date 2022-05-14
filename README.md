![](./.github/banner.png)

<p align="center">
  A script to factorize integers with sagemath and factordb.
  <br>
  <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/p0dalirius/factorizator">
  <a href="https://twitter.com/intent/follow?screen_name=podalirius_" title="Follow"><img src="https://img.shields.io/twitter/follow/podalirius_?label=Podalirius&style=social"></a>
  <a href="https://www.youtube.com/c/Podalirius_?sub_confirmation=1" title="Subscribe"><img alt="YouTube Channel Subscribers" src="https://img.shields.io/youtube/channel/subscribers/UCF_x5O7CSfr82AfNVTKOv_A?style=social"></a>
  <br>
</p>

## Features

 - [x] Automatically checks if the number is already factored in [factordb.com](https://factordb.com).
 - [x] Local factorization with sagemath.
 - [x] Export the found factors to `factors.json`.

## Requirements

Install the following requirements for the script to work properly:

```
sudo apt install sagemath
python3 -m pip install requirements.txt
```

## Usage

```
$ ./facto.sage.py -h
  _____          _             _          _
 |  ___|_ _  ___| |_ ___  _ __(_)______ _| |_ ___  _ __
 | |_ / _` |/ __| __/ _ \| '__| |_  / _` | __/ _ \| '__|  v1.3
 |  _| (_| | (__| || (_) | |  | |/ / (_| | || (_) | |
 |_|  \__,_|\___|\__\___/|_|  |_/___\__,_|\__\___/|_|     by @podalirius_


usage: facto.sage.py [-h] -n NUMBER

Factorize an integer.

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        Integer to factorize.
```

## Contributing

Pull requests are welcome. Feel free to open an issue if you want to add other features.
