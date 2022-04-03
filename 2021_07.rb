require 'logger'

AOCDAY = 7
AOCYEAR = 2021

def calculate_fuel_part1(start_position, final_position)
  # calculate fuel used when moving from start_position to final_position
  #  this is just the distance
  (final_position - start_position).abs
end

def calculate_fuel_part2(start_position, final_position)
  # calculate fuel used when moving from start_position to final_position
  #  This is the sum of 1..distance
  retval = (1..(final_position - start_position).abs).inject(0) {
    |retval, x| retval += x }
end


def run(inputfile, logger, **kwargs)
  positions = []
  File.open(inputfile).each_line do |line|
    positions = line.split(',').map(&:to_i)
  end

  calculate_fuel_method = (kwargs.include? :part2) ? :calculate_fuel_part2 : :calculate_fuel_part1

  # find min and max possible horizontal positions
  position_min = 0
  position_max = positions.sort.max

  # calculate fuel used at every position; preserve least fuel used
  #  initialize minimum with fuel used at position_max
  best_position = position_max
  calculated_fuel_min = positions.inject(0) {
    |calculated_fuel, newpos| calculated_fuel += send(calculate_fuel_method, newpos, best_position) };

  #  calculate fuel used at every other position, preserve minimum
  (position_min..position_max - 1).each do |final_position|
    calculated_fuel = positions.inject(0) {
      |calculated_fuel, newpos| calculated_fuel += send(calculate_fuel_method, newpos, final_position) };
    logger.debug("-- position #{final_position} uses #{calculated_fuel} fuel")
    if calculated_fuel < calculated_fuel_min
      best_position = final_position
      calculated_fuel_min = calculated_fuel
    end
  end

  puts("Best position #{best_position} uses #{calculated_fuel_min} fuel.");
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
