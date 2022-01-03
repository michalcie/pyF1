---
layout: home
---

Something for F1 passionate. 

Checkout github repository  <github repositoiry>
... or have a look at what it is used for <first post>

## Intro

pyF1 python project provides some functions that makes analysing F1 a bit easier
It uses telemetry and other data provided <<fastf1> by theOehrly> and presents it
in a more digestable way. However, you can find here much more, as I will be posting
here some F1 related analysis with source code available in the repo - something for
real nerds. 


## Demo

A brief demonstration of what it is all about.


Let's say that we would like to see how dominant was Red Bull pace in 2021 Mexico GP.
We can use this short code:
```
from path.source import track_telemetry as tt
laps, event = tt.crate_event(2021, 'Mexico', 'R') #No mistake as of now 13.11.2021 'USA' returns Mexico City GP - issue#23
drivers_list = ['VER', 'HAM', 'PER','BOT']

tt.ridgeline(drivers_list, laps, "Mexico 2021 - How Fast was Redbull?", None, None, 0)
```

The output is the following graph

## Documentation
Some basic docs can be found in <doc> post

## License

Copyright 2022 michalcie.

Built with theme <gitbook>  
[![Jekyll Themes](https://img.shields.io/badge/featured%20on-JekyllThemes-red.svg)](https://jekyll-themes.com/jekyll-gitbook/)