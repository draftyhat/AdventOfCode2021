require 'logger'
require_relative 'lib/grid'

AOCDAY = 9
AOCYEAR = 2021

def run(inputfile, logger, **kwargs)
  # read in grid
  g = Grid.new(File.open(inputfile), single_character: true)

  sumlowpoints = 0
  (0...g.width).each do |x|
    (0...g.height).each do |y|
      logger.debug("traversing (#{x},#{y})");
      left = g.get(x-1, y, default: 10);
      right = g.get(x+1, y, default: 10);
      up = g.get(x, y+1, default: 10);
      down = g.get(x, y-1, default: 10);
      val = g.get(x,y);

      if (val < left) && (val < right) && (val < up) && (val < down)
        logger.debug("Found low point #{val} at #{x},#{y}");
        sumlowpoints += val + 1;
      end
    end
  end

  puts("Found low points sum #{sumlowpoints}")
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
