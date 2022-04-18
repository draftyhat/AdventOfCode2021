require 'logger'
require_relative 'lib/grid'

AOCDAY = 9
AOCYEAR = 2021

def run(inputfile, logger, **kwargs)
  # read in grid
  grid = Grid.new(fh: File.open(inputfile), single_character: true)

  sumlowpoints = 0
  (0...grid.width).each do |x|
    (0...grid.height).each do |y|
      logger.debug("traversing (#{x},#{y})");
      left = grid.get(x-1, y, default: 10);
      right = grid.get(x+1, y, default: 10);
      up = grid.get(x, y+1, default: 10);
      down = grid.get(x, y-1, default: 10);
      val = grid.get(x,y);

      if (val < left) && (val < right) && (val < up) && (val < down)
        logger.debug("Found low point #{val} at #{x},#{y}");
        sumlowpoints += val + 1;
      end
    end
  end

  puts("Found low points sum #{sumlowpoints}")
end

def process_basin(grid, x, y)
  # process the basin starting at x,y in grid grid
  #   set all elements to 10
  #   return basin size
  pointstack = [[x,y]]
  basinsize = 0;

  nextpoint = pointstack.pop()
  while not nextpoint.nil?
    x,y = nextpoint
    begin
      val = grid.get(x, y, default: 10)
      # is this element part of the basin?
      if val < 9
        # mark this point as part of the basin
        grid.set(x, y, 10)
        basinsize += 1

        # check points around this point next
        pointstack.push([x-1, y])
        pointstack.push([x+1, y])
        pointstack.push([x, y-1])
        pointstack.push([x, y+1])
      end
    rescue GridBoundaryError => err
    end
    nextpoint = pointstack.pop()
  end

  # return the basin size
  basinsize
end

def run_part2(inputfile, logger, **kwargs)
  # read in grid
  grid = Grid.new(fh: File.open(inputfile), single_character: true)

  basinsizes = []
  # find next basin
  (0...grid.width).each do |x|
    (0...grid.height).each do |y|
      val = grid.get(x, y, default:10)
      if val < 9
        # this is a new basin. Calculate size
        basinsizes << process_basin(grid, x, y)
      end
    end
  end

  # multiply sizes of three largest basins
  answer = basinsizes.sort().reverse[0..2].inject(1) {|ret, x| x*ret}
  puts("Part 2 answer #{answer}");

  answer
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
    run_part2(inputfile, logger, **options)
  end
end
