require 'logger'

AOCDAY = 12
AOCYEAR = 2021

class Cave
  attr_accessor :name
  attr_accessor :small

  def initialize(name, logger)
    @name = name
    @logger = logger
    @small = false
    if name.downcase == name
      @small = true
    end
    @connections = []
  end

  def add_connection(other)
    @connections << other
    @connections.sort()
  end

  def <=>(other)
    @name <=> other.name
  end

  def to_s()
    return @name
  end

  def get_n_paths(path, part2: false)
    small_cave_visits_allowed = part2 ? 2:1
    npaths = 0

    # for each cave we're connected to
    @connections.each do |nextcave|
      @logger.debug("Cave<#{@name}> checking connection #{nextcave}");
      # check to see if this is a valid next step
      if nextcave.name == 'start'
        #   start can only be visited once
      elsif nextcave.name == 'end'
        #   ends this path
        @logger.debug("Path: #{path.map(&:to_s).join(',')}");
        npaths += 1
      elsif nextcave.small
        #   small caves can't be visited more than once
        nextcaves_in_path =  path.select {|x| x.name == nextcave.name }
        if nextcaves_in_path.length < small_cave_visits_allowed
          npaths += nextcave.get_n_paths(path.clone() + [nextcave], part2: part2);
        end
      else
        #   large cave. Do it.
        npaths += nextcave.get_n_paths(path.clone() + [nextcave], part2: part2);
      end
    end
    npaths
  end
end

def run(inputfile, logger, **kwargs)
  caves = {}

  File.open(inputfile).each_line do |line|
    # read two names
    first,last = line.strip.split('-')
    # figure out if we have them already
    if caves.has_key? first
      first_cave = caves[first]
    else
      first_cave = caves[first] = Cave.new(first, logger)
    end
    if caves.has_key? last
      last_cave = caves[last]
    else
      last_cave = caves[last] = Cave.new(last, logger)
    end

    first_cave.add_connection(last_cave)
    last_cave.add_connection(first_cave)
  end

  # beginning at start position, traverse caves
  start = caves["start"]
  npaths = start.get_n_paths([start], part2: kwargs.include?(:part2))
  puts("Found #{npaths} paths!");
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
