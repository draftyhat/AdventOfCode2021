require 'logger'
require 'scanf'

AOCDAY = 14
AOCYEAR = 2021

class Polymer
  def initialize(fh, logger)
    # initialize by reading in initial string and expansion rules
    #  initial string
    @pairs = {}
    @pairs.default = 0
    initial_string = fh.readline.strip
    (1...initial_string.length).each do |endidx|
      @pairs[initial_string[endidx - 1..endidx]] += 1
    end
    @firstletter = initial_string[0]

    #  skip blank line
    line = fh.readline

    #  expansion rules
    @rules = {}
    fh.each_line do |line|
      pair, addch = line.strip.scanf("%2s -> %c")
      @rules[pair] = [pair[0] + addch, addch + pair[1]]
    end

    @logger = logger
    @logger.debug("Rules: #{@rules}");
    @logger.debug("Initial pairs: #{@pairs}");
    @step = 0
  end

  def step()
    newpairs = {}
    newpairs.default = 0
    @pairs.each do |oldpair, n|
      # expand this pair
      newpair1, newpair2 = @rules[oldpair]
      @logger.debug("#{oldpair} -> #{newpair1}, #{newpair2} #{n}");
      # record new amounts
      newpairs[newpair1] += n
      newpairs[newpair2] += n
    end
    @pairs = newpairs
    @step += 1
    @logger.debug("Step #{@step}: #{@pairs}")
  end

  def answer
    # count of most common element - count of least common element

    # calculate count for each element. Note we only count the second letter of
    # each pair. The first letter in the string remains constant, so we
    # count that as a special case.
    elementcount = { @firstletter => 1 }
    elementcount.default = 0
    @pairs.each do |pair, newcount|
      elementcount[pair[1]] += newcount
    end
    @logger.debug("Total element counts: #{elementcount}")

    # calculate most common element - least common element
    #   one pass, rather than using ruby min/max (2 passes)
    puts elementcount
    mincount = maxcount = elementcount.first[1]
    elementcount.each do |element, ecount|
      maxcount = [ecount, maxcount].max
      mincount = [ecount, mincount].min
    end
    maxcount - mincount
  end
end


def run(inputfile, logger, **kwargs)
  polymer = nil
  File.open(inputfile) do |fh|
    polymer = Polymer.new(fh, logger)
  end

  (1..10).each do
    polymer.step
  end
  puts("Count at step 10: #{polymer.answer}")

  (11..40).each do
    polymer.step
  end
  puts("Count at step 40: #{polymer.answer}")
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
