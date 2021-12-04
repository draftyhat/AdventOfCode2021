import sys;
import bisect;


# read in the input
ints = []
inputline = sys.stdin.readline();
valuelength = len(inputline) - 1;
while(len(inputline) > 0):
    ints.append(int(inputline, 2));
    inputline = sys.stdin.readline();

# sort the array
ints.sort();

print("valuelength: {}".format(valuelength));
print("first split at {}".format((1 << (valuelength - 1)) - 1));

# find the point at which the first digit changes from 0 to 1
firstbitsplit = bisect.bisect(ints, (1 << (valuelength - 1)) - 1);
if(firstbitsplit > len(ints)/2):
    oglist = ints[:firstbitsplit];
    co2list = ints[firstbitsplit:];
    ogsplit = 0;
    co2split = (1 << (valuelength - 1)) - 1;
else:
    oglist = ints[firstbitsplit:];
    co2list = ints[:firstbitsplit];
    ogsplit = (1 << (valuelength - 1)) - 1;
    co2split = 0;

print("oglist length: {}".format(len(oglist)));
print("co2list length: {}".format(len(co2list)));

# find the oxygen generator rating. The array is sorted, and we throw away
# irrelevant numbers at each step, so the most common digit in the nth column
# will always be the digit in the number at the halfway point. Or, to put it a
# different way, if you find the point at which the nth digit changes to 1, if
# that's less than halfway it's the least common digit in that column; if it's
# past halfway, it's the most common.
ogdigit = 2;
while(len(oglist) > 1):
    print("oglist: {}".format(','.join(['{:0b}'.format(x) for x in oglist])));
    # find the spot where the first digit switches from 1 to 0
    split = bisect.bisect(oglist, ogsplit + (1 << (valuelength - ogdigit)))
    print("  split at {}, index {} (list length {})".format((1 << (valuelength - ogdigit)) - 1, split, len(oglist)));
    if(split > len(oglist)/2):
        oglist = oglist[:split]
    else:
        oglist = oglist[split:]
        ogsplit += 1 << (valuelength - ogdigit)
    ogdigit += 1;

co2digit = 2;
while(len(co2list) > 1):
    print("co2list: {}".format(','.join(['{:0b}'.format(x) for x in co2list])));
    # find the spot where the first digit switches from 1 to 0
    split = bisect.bisect(co2list, co2split + (1 << (valuelength - co2digit)))
    print("  split at {}, index {} (list length {})".format((1 << (valuelength - co2digit)) - 1, split, len(co2list)));
    if(split <= len(co2list)/2):
        co2list = co2list[:split]
    else:
        co2list = co2list[split:]
        co2split += 1 << (valuelength - co2digit)
    co2digit += 1;

print(oglist)
print(co2list)
print(oglist[0] * co2list[0]);
