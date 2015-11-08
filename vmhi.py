#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Shows the processes using swap space."""

import os
import os.path
import string

def get_vm_usage(path):
    """Return (Name, VmSize, VmSwap) for process status in path."""
    stats = {}
    
    # gather all status attributes as {key: [value]} for a process
    with open(path) as inf:
        for line in inf:
            fields = line.split()
            stats[fields[0][:-1]] = fields[1:]

    return (stats['Name'][0], stats['VmSize'][0],
           stats['VmSwap'][0])


def proc_stats(path='/proc'):
    """Yields numeric pathnames in path"""
    for name in os.listdir(path):
        if name.isdigit():
            statf = os.path.join(path, name, 'status')
            yield statf

def main():
    procs = []
    for p in proc_stats():
        try:
            procs.append(get_vm_usage(p))
        except KeyError as e:
            # there are threads which have no VmSize, ignore them
            pass 

    # order by descenting swap use
    procs.sort(key=lambda p: int(p[2]), reverse=True)

    print('{:>8s} {:>7s} {}'.format('Size MB', 'Swap MB', 'name'))
    for (name, size, swap) in procs:
        # only show process that are using swap
        if int(swap) > 0:
            print('{:8.3f} {:7.3f} {}'.format(int(size)/1000.0,
                int(swap)/1000.0, name))



if __name__ == '__main__': main()
