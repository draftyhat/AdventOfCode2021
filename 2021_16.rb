require 'logger'

AOCDAY = 16
AOCYEAR = 2021

# 3-bit version number
# 3-bit type
#   type 0: sum
#   type 1: product
#   type 2: minimum
#   type 3: minimum
#   type 4: literal
#   type 5: greater than
#   type 6: less than
#   type 7: equal to
#   all operator packets (all but 4) format:
#     1-bit length type ID. 0 == 15 bit number, 1 == 11-bit number
#     n-bit subpacket
#   literal packet format:
#     5-bit groups, 1 bit continuation and 4 bit value
#
# "pos"es are [byte index, bit number], where msb is 0

def get_n_bits(s, pos, n)
  # returns [endpos, value]
  nibblepos, bitpos = pos
  value = 0;

  # process bits at the beginning of the string
  if bitpos > 0
    value += (0xf >> bitpos) & s[nibblepos].to_i(16);
    if n < (4-bitpos)
      # oops, we just slurped up too many bits
      value >>= (4 - bitpos - n)
      bitpos += n;
      n = 0
    else
      n -= (4-bitpos);
      nibblepos += 1;
      bitpos = 0;
    end
  end

  # process full nibbles
  while n > 4
    value = (value << 4) + s[nibblepos].to_i(16)
    nibblepos += 1
    n -= 4
  end

  # process leftover bits
  if n > 0
    value = (value << n) + (s[nibblepos].to_i(16) >> (4-n));
    bitpos = n
    if bitpos >= 4
      nibblepos += 1;
      bitpos -= 4;
    end
  end

  return [[nibblepos, bitpos], value]
end

def parse_version_type(s, pos)
  # returns [endpos, version, type]
  endpos, version = get_n_bits(s, pos, 3)
  endpos, type = get_n_bits(s, endpos, 3)
  return endpos, version, type
end

def parse_literal(s, pos)
  # returns [endpos, value]
  keepgoing = 1
  value = 0
  endpos = pos
  while 1 == keepgoing
    endpos, keepgoing = get_n_bits(s, endpos, 1)
    endpos, thesebits = get_n_bits(s, endpos, 4)
    value = (value << 4) + thesebits
  end

  return endpos, value
end

def parse_operator(s, pos)
  # returns endpos, versionsum, [values]
  endpos, length_type_id = get_n_bits(s, pos, 1);
  nextlen = (1 == length_type_id) ? 11 : 15
  endpos, sublen = get_n_bits(s, endpos, nextlen);

  versionsum = 0

  # if length_type_id is 1, parse sublen sub-packets
  values = []
  if 1 == length_type_id
    (0...sublen).each do |subpacketn|
      endpos, new_versionsum, new_value = parse(s, endpos)
      versionsum += new_versionsum
      values << new_value
    end
  else
    # else, length_type_id is 0. Parse sublen bits worth of packets.
    nibblepos, bitpos = endpos;
    subend_nibblepos = nibblepos + (bitpos + sublen).div(4);
    subend_bitpos = (bitpos + sublen) % 4

    while (nibblepos < subend_nibblepos) \
        or ((nibblepos == subend_nibblepos) and (bitpos < subend_bitpos))
      endpos, new_versionsum, new_value = parse(s, endpos);
      versionsum += new_versionsum
      values << new_value
      nibblepos, bitpos = endpos
    end
  end
  return endpos, versionsum, values
end

def parse(s, pos)
  # returns endpos, versionsum, value
  versionsum = 0
  endpos, version, type = parse_version_type(s, pos);
  versionsum += version;
  value = 0

  if type == 4
    endpos, value = parse_literal(s, endpos)
  else
    # operator
    endpos, new_versionsum, values = parse_operator(s, endpos)
    versionsum += new_versionsum

    case type
    when 0        # sum
      value = values.sum
    when 1        # product
      value = values.inject(1) {|x,y| x*y}
    when 2        # minimum
      value = values.min
    when 3        # maximum
      value = values.max
    when 5        # greaater than
      value = (values[0] > values[1]) ? 1 : 0
    when 6        # less than
      value = (values[0] < values[1]) ? 1 : 0
    when 7        # equal to
      value = (values[0] == values[1]) ? 1 : 0
    end
  end

  return endpos, versionsum, value
end


def run(inputfile, logger, **kwargs)
  data = '';
  File.open(inputfile) do |fh|
    data = fh.readline
  end

  endpos, versionsum, value = parse(data, [0,0])
  puts("Found version sum #{versionsum}");
  puts("Found result #{value}");
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

  ARGV.each do |inputfile|
    run(inputfile, logger, **options)
  end
end
