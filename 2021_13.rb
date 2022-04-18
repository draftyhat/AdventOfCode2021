require 'logger'
require 'scanf'
require_relative 'lib/grid'

AOCDAY = 13
AOCYEAR = 2021

# count number of dots
def sumfunc(sum, n)
  sum += n == '#' ? 1 : 0
end

def run(inputfile, logger, **kwargs)
  dots = []
  folds = []

  File.open(inputfile) do |fh|
    # read dot coordinates
    line = fh.readline
    while line.strip.length > 0
      dots.append(line.strip.split(',').map(&:to_i))
      line = fh.readline
    end

    # read folds
    fh.each_line.each do |line|
      folds.append(line.strip.scanf('fold along %c=%d'))
    end
  end

  # create grid and apply dots
  xmax = dots.max { |point0, point1| point0[0] <=> point1[0] } [0] + 1
  ymax = dots.max { |point0, point1| point0[1] <=> point1[1] } [1] + 1
  grid = Grid.new(width: xmax, height: ymax, default: ' ', delimiter: '')

  dots.each do |x,y|
    grid.set(x, y, '#')
  end

  # fold   result: scalar - (y - scalar) = 2 * scalar - y
  folds.each_with_index do |axisnscalar, nfolds|
    axis, scalar = axisnscalar
    logger.debug("Folding at #{axis}=#{scalar}");
    if 'x' == axis
      # hopefully no folds where scalar < ymax/2
      (scalar...xmax).each do |x|
        (0...ymax).each do |y|
          if '#' == grid.get(x,y)
            logger.debug("Folding (#{x},#{y}) to (#{2 * scalar - x},#{y})");
            grid.set(2 * scalar - x, y, '#')
            grid.set(x, y, ' ');
          end
        end
      end
      xmax = scalar + 1
    else     # y axis
      (scalar...ymax).each do |y|
        (0...xmax).each do |x|
          if '#' == grid.get(x,y)
            logger.debug("Folding (#{x},#{y}) to (#{x},#{2 * scalar - y})");
            grid.set(x, 2 * scalar - y, '#')
            grid.set(x, y, ' ');
          end
        end
      end
      ymax = scalar + 1
    end
    logger.debug("\n" + grid.to_s_subgrid(xmax:xmax, ymax:ymax) + "\n");
    if 0 == nfolds
      puts("#{grid.sum_subgrid(xmax:xmax, ymax:ymax, p: :sumfunc)} dots after 1st fold")
    end
  end

  sum = grid.sum_subgrid(xmax:xmax, ymax:ymax, p: :sumfunc)
  puts("Found #{sum} marked spots");

  # print
  puts grid.to_s_subgrid(xmax:xmax, ymax:ymax);
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
