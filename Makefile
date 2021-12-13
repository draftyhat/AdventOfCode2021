# make day 1 executable: make 1
# make day 1 executable, part 2: make 1p2
# make day 1 debug executable: make 1
# make day 1 debug executable, part 2: make debug1p2

CC = gcc
_CFLAGS = $(CFLAGS) -Wall
YEAR=2021

all: 1

debug%:
	make CFLAGS="-DDEBUG $(CFLAGS)" $*
%p2:
	make CFLAGS="-DPART2 $(CFLAGS)" $*

$(YEAR)_01 $(YEAR)_02 $(YEAR)_03 $(YEAR)_04 $(YEAR)_05 $(YEAR)_06 $(YEAR)_07 $(YEAR)_08 $(YEAR)_09 $(YEAR)_10 $(YEAR)_12 $(YEAR)_14 $(YEAR)_15 $(YEAR)_16 $(YEAR)_17 $(YEAR)_18 $(YEAR)_19 $(YEAR)_21 $(YEAR)_22 $(YEAR)_23 $(YEAR)_24 $(YEAR)_25: %: %.c
	$(CC) $(DEBUG) $(_CFLAGS) -o $@ $<
$(YEAR)_11 $(YEAR)_13: %: %.o grid.o
	$(CC) $(DEBUG) $(_CFLAGS) -o $@ $^

test%: %
	cat test/$(YEAR)_`printf %02d $*`_test | ./$(YEAR)_`printf %02d $*`

1 2 3 4 5 6 7 8 9: %: $(YEAR)_0%
10 11 12 13 14 15 16 17 18 19: %: $(YEAR)_%
20 21 22 23 24 25 26 27 28 29: %: $(YEAR)_%
30 31: %: $(YEAR)_%

test%: $(YEAR)_%
	cat test/${^}_test | ./$^

test1 test2 test3 test4 test5 test6 test7 test8 test9: test%: test0%
test10 test11 test12 test13 test14 test15 test16 test17 test18 test19: test%: $(YEAR)_%
test20 test21 test22 test23 test24 test25 test26 test27 test28 test29: test%: $(YEAR)_%
test30 test31: test%: $(YEAR)_%

grid.o: lib/grid.c include/grid.h
	$(CC) -c $(_CFLAGS) -Iinclude -o $@ $<

$(YEAR)_%.o: $(YEAR)_%.c
	$(CC) -c $(_CFLAGS) -Iinclude -o $@ $<



clean:
	rm -f *.o
	rm -f $(YEAR)_[0-3][0-9]
	rm -f $(YEAR)_[0-3][0-9]p2

