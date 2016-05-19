#!/bin/env python

import profile
from pstats import Stats
from Main import main

s = profile.run('main()', 'pksampler.profile')
Stats('pksampler.profile').sort_stats('calls').print_stats()
