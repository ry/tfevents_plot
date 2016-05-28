#!/usr/bin/env python
# This script makes a plot comparing tensorflow tfevent log files
# Example usage: 
# tfevents_plot.py loss_avg before:/Users/ryan/src/gym/before.tfevents batch:/Users/ryan/src/gym/batch.tfevents batch_norm:/tmp/agent_train/events.out.tfevents.1464449636.yyy.local

import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.python.summary.event_multiplexer import EventMultiplexer

matplotlib.style.use('ggplot')


def parse_arg(arg):
    """Returns (run, tfevents_path)"""
    parts = arg.split(':')
    if len(parts) == 1:
        path = parts[0]
        basename = os.path.basename(path)
        return (basename, path)
    elif len(parts) == 2:
        return parts
    else:
        print "bad arg", arg
        sys.exit(1)


def parse_args():
    script_name = sys.argv[0]
    args = sys.argv[1:]

    if len(args) < 2:
        print "usage: %s [scalar summary tag] 1.tfevents 2.tfevents"
        sys.exit(1)

    tag = args.pop(0)

    run_path_map = {}

    for arg in args:
        run, path = parse_arg(arg)
        run_path_map[run] = path

    return tag, run_path_map


def plot_run(mux, tag, run, ax):
    if not tag in mux.Runs()[run]['scalars']:
        print "Bad scalar tag '%s'." % tag
        print "Good values:", mux.Runs()[run]['scalars']
        sys.exit(1)

    events = mux.Scalars(run, tag)

    start_time = events[0].wall_time

    x = np.zeros(len(events))
    y = np.zeros(len(events))

    for i, ev in enumerate(events):
        y[i] = ev.value
        rel_time = ev.wall_time - start_time
        x[i] = rel_time
    ax.plot(x, y)


def main():
    tag, run_path_map = parse_args()
    mux = EventMultiplexer(run_path_map)
    mux.Reload()

    #print "tags", mux.Tags()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(tag)
    ax.set_xlabel("rel time")

    runs = run_path_map.keys()
    for run in runs:
        plot_run(mux, tag, run, ax)

    plt.legend(runs, loc='lower right')
    plt.show()


if __name__ == "__main__":
    main()
