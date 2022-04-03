require 'logger'
require 'set'

AOCDAY = 8
AOCYEAR = 2021

# record of the number of segments in a given digit (indexed by digit value)
NSEGMENTS_ZERO = 6
NSEGMENTS_ONE = 2
NSEGMENTS_TWO = 5
NSEGMENTS_THREE = 5
NSEGMENTS_FOUR = 4
NSEGMENTS_FIVE = 5
NSEGMENTS_SIX = 6
NSEGMENTS_SEVEN = 3
NSEGMENTS_EIGHT = 7
NSEGMENTS_NINE = 6

# these constants allow us to use math to determine the match between number of
# segments. In short, we use a base8 number.
BASE1 = 1
BASE4 = 8
BASE7 = 64

# non-unique numbers
#  5 segments: 2, 3, 5
#    ----    ----    ----
#        -       -  =
#        -       -  =
#    ----    ----    ----
#   -            -       -
#   -            -       -
#    ----    ----    ----
#  6 segments: 0, 6, 9
#    ----    ----    ----
#   -    -  -       -    -
#   -    -  -       -    -
#            ----    ----
#   -    -  -    -       -
#   -    -  -    -       -
#    ----    ----    ----
#  unique numbers
#                    ----    ----
#        -  -    -       -  -    -
#        -  -    -       -  -    -
#            ----            ----
#        -       -       -  -    -
#        -       -       -  -    -
#                            ----
# 5-segment number overlaps:
#   2 overlaps 1 in 1 segments
#   2 overlaps 4 in 2 segments
#   2 overlaps 7 in 2 segments
#   3 overlaps 1 in 2 segments
#   3 overlaps 4 in 3 segments
#   3 overlaps 7 in 3 segments
#   5 overlaps 1 in 1 segments
#   5 overlaps 4 in 3 segments
#   5 overlaps 7 in 2 segments
Five_segment_overlaps = {
  # overlaps with two
  1 * BASE1 + 2 * BASE4 => 2,
  # overlaps with three
  2 * BASE1 + 3 * BASE4 => 3,
  # overlaps with five
  1 * BASE1 + 3 * BASE4 => 5,
}

# 6-segment number overlaps:
#   0 overlaps 1 in 2 segments
#   0 overlaps 4 in 2 segments
#   6 overlaps 1 in 1 segments
#   6 overlaps 4 in 3 segments
#   9 overlaps 1 in 1 segments
#   9 overlaps 4 in 4 segments
Six_segment_overlaps = {
  # overlaps with zero
  2 * BASE1 + 3 * BASE4 => 0,
  # overlaps with six
  1 * BASE1 + 3 * BASE4 => 6,
  # overlaps with nine
  2 * BASE1 + 4 * BASE4 => 9,
}
  

def determine_number(s, one, four, seven, segment_overlap)
  # given the sequences for one, four, and seven, determine which
  # number is given by the character sequence s
  s_set = Set.new(s.split(''))
  # calculate the base8 number that determines our match
  #puts("-- s: #{s} #{s.class}  s.split #{s.split("")}  set: #{s_set}")
  intersect_value = \
    s_set.intersection(Set.new(one.split(''))).length * BASE1 \
    + s_set.intersection(Set.new(four.split(''))).length * BASE4

  #puts("-- sequence #{s} intersect_value #{intersect_value}  overlaps #{segment_overlap}");
  return segment_overlap[intersect_value];
end

def determine_5segment_number(s, one, four, seven)
  # given the sequences for one, four, and seven, determine which 5-segment
  # number is given by the character sequence s
  determine_number(s, one, four, seven, Five_segment_overlaps)
end

def determine_6segment_number(s, one, four, seven)
  # given the sequences for one, four, and seven, determine which 6-segment
  # number is given by the character sequence s
  determine_number(s, one, four, seven, Six_segment_overlaps)
end
  
def run_part2(inputfile, logger, **kwargs)
  sum = 0;

  # read in each line
  File.open(inputfile).each_line do |line|
    inputs,outputs = line.split("|");
    inputlist = []
    outputlist = []
    inputlist << inputs.split(' ');
    outputlist << outputs.split(' ');

    #  determine sequences for 1, 4, 7, 8
    known_sequences = {}
    known_digits = {}
    need1478 = {
      NSEGMENTS_ONE => 1,
      NSEGMENTS_FOUR => 4,
      NSEGMENTS_SEVEN => 7,
      NSEGMENTS_EIGHT => 8 };
    logger.debug("-------- determining sequences for 1,4,7,8");
    inputlist.each do |sequences|
      sequences.each do |sequence|
        # find sequences for 1, 4, 7, 8, the unique-number-of-segments digits
        slen = sequence.length
        logger.debug("  sequence #{sequence} need1478 #{need1478}");
        sequence_digit = need1478.delete(slen)
        if not sequence_digit.nil?
          known_sequences[sequence.chars.sort.join()] = sequence_digit;
          known_digits[sequence_digit] = sequence;
        end

        # check to see if we're done
        break if 0 == need1478.length
      end
      # check to see if we're done
      break if 0 == need1478.length
    end

    # determine sequences for the other numbers
    logger.debug("-------- determining rest of sequences");
    logger.debug("  known_sequences: #{known_sequences}");
    need_others = Hash.new {|h,k| h[k]=[]}
    need_others[NSEGMENTS_ZERO] << 0
    need_others[NSEGMENTS_TWO] << 2
    need_others[NSEGMENTS_THREE] << 3
    need_others[NSEGMENTS_FIVE] << 5
    need_others[NSEGMENTS_SIX] << 6
    need_others[NSEGMENTS_NINE] << 9
    nunknowndigits = 6

    segmentset_one = Set.new(known_digits[1].split(''));
    segmentset_four = Set.new(known_digits[4].split(''));
    inputlist.each do |sequences|
      sequences.each do |sequence|
        # skip sequences we already know
        next if (known_sequences.has_key? sequence.chars.sort.join);

        sequenceset = Set.new(sequence.split(''));

        overlapnumber = sequenceset.intersection(segmentset_one).length * BASE1 + \
          sequenceset.intersection(segmentset_four).length * BASE4;
        determine_number_method = (5 == sequence.length) ? :determine_5segment_number : :determine_6segment_number;
        digit = send(determine_number_method, sequence, known_digits[1],
                     known_digits[4], known_digits[7]);
        known_sequences[sequence.chars.sort.join] = digit;
        nunknowndigits -= 1;

        # check to see if we're done
        break if (0 == nunknowndigits)
      end
      # check to see if we're done
      break if (0 == nunknowndigits)
    end

    # now we know all the digits. Calculate the sum.
    logger.debug("-------- calculating sum");
    logger.debug("  known_sequences: #{known_sequences}");

    outputlist.each do |outputs|
      puts(outputs);
      sum += outputs.inject(0) { |retval, s| retval = retval * 10 + known_sequences[s.chars.sort.join] }
    end

  end
  puts("sum of all displayed numbers: #{sum}")
  sum
end

def run_part1(inputfile, logger, **kwargs)
  n1478s = 0
  File.open(inputfile).each_line do |line|
    input,output = line.split("|");
    outputs = output.split(' ');
    logger.debug(outputs)
    n1478s += outputs.inject(0) { |retval, x|
      puts("  output #{x}, length #{x.length}");
      retval += ([NSEGMENTS_ONE, NSEGMENTS_FOUR, NSEGMENTS_SEVEN, NSEGMENTS_EIGHT ].include? x.length) ? 1 : 0
    }
  end

  puts("Found #{n1478s} uniquely segmented digits");
end


if __FILE__ == $0
  require 'optparse'

  options = {}
  OptionParser.new do |opts|
    opts.banner = "Usage: $0 [options] <inputfile> [<more inputfiles>]\n" \
      "  Advent of Code #{AOCYEAR} day #{AOCDAY}"

    opts.on("-v", "--verbose", "Be verbose") do |v|
      options[:verbose] = v
    end

    opts.on("-2", "--part2", "Run part 2") do |part2|
      options[:part2] = true
    end

    opts.on("-h", "--help", "Print this help message") do
      puts opts
      exit
    end
  end.parse!

  logger = Logger.new(STDOUT);
  logger.level = (options.include? :verbose) ? Logger::DEBUG : Logger::WARN

  runmethod = (options.include? :part2) ? :run_part2 : :run_part1
  ARGV.each do |inputfile|
    send(runmethod, inputfile, logger, **options)
  end
end
