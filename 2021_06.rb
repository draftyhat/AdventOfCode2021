require 'logger'

AOCDAY = 6
AOCYEAR = 2021

# oh my word! It's the dreaded lanternfish!

def run(logger, **kwargs)
  ndays = (kwargs.include? :part2) ? 256 : 80

  # starting vector
  fishages = [3,4,3,1,2]

  # create initial array of number of fish at each age
  nfishperage = [0]*9
  fishages.each do |age|
    nfishperage[age] += 1
  end

  logger.debug("Starting nfishperage: #{nfishperage}");

  # iterate day by day, saving the number of fish at each age
  (0...ndays).each do |day|
    new_nfishperage = [0]*9
    # do age 0 as a special case
    logger.debug("  adding #{nfishperage[0]} age 7");
    logger.debug("  adding #{nfishperage[0]} age 9");
    new_nfishperage[6] = new_nfishperage[8] = nfishperage[0];
    nfishperage[1,8].each_with_index do |nfish, age|
      # age is already age - 1 because of the nfishperage slice
      logger.debug("  adding #{nfish} age #{(age)}");
      new_nfishperage[age] += nfish
    end

    nfishperage = new_nfishperage;
    logger.debug("day #{day}: #{nfishperage}");
  end

  puts("Answer: #{nfishperage.sum} fish")
end


if __FILE__ == $0
  require 'optparse'

  options = {}
  OptionParser.new do |opts|
    opts.banner = "Usage: $0 [options]\n" \
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

  run(logger, **options)
end
