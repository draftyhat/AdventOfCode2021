require 'logger'
require_relative 'lib/grid'

AOCDAY = 20
AOCYEAR = 2021

def subgrid_to_index(grid, defaultpixel, x, y)
  value = 0
  value = (value << 1) + grid.get(x-1, y-1, default:defaultpixel)
  value = (value << 1) + grid.get(x  , y-1, default:defaultpixel)
  value = (value << 1) + grid.get(x+1, y-1, default:defaultpixel)
  value = (value << 1) + grid.get(x-1, y  , default:defaultpixel)
  value = (value << 1) + grid.get(x  , y  , default:defaultpixel)
  value = (value << 1) + grid.get(x+1, y  , default:defaultpixel)
  value = (value << 1) + grid.get(x-1, y+1, default:defaultpixel)
  value = (value << 1) + grid.get(x  , y+1, default:defaultpixel)
  value = (value << 1) + grid.get(x+1, y+1, default:defaultpixel)
  value
end

def run(inputfile, logger, **kwargs)
  iea=''
  grid = nil
  File.open(inputfile) do |fh|
    # read image enhancement algorithm, convert to 0s and 1s
    iea = fh.readline.strip.gsub(/[.#]/, {'.'=>0,'#'=>1}).split('').map(&:to_i)
    fh.readline

    # read grid, converting to 0s and 1s
    grid = Grid.new(fh: fh, single_character: true,
                    translation_pattern: /[.#]/,
                    translation_map: {'.'=>0,'#'=>1});

  end

  # set the number of enhancements
  nsteps = kwargs.include?(:part2) ? 50 : 2

  # the image will expand by nsteps*2 pixels in each direction. Resize the grid
  # to account for that.
  grid.resize!(grid.width + nsteps * 4, grid.height + nsteps * 4,
               newx0: nsteps * 2, newy0: nsteps * 2, default: 0)
  logger.debug("Original grid:\n#{grid}")

  # enhance nsteps times
  defaultpixel = 0
  (0...nsteps).each do |step|
    newgrid = Grid.new(width: grid.width, height: grid.height, default: 0, single_character: true)
    (0...grid.width).each do |x|
      (0...grid.height).each do |y|
        newgrid.set(x, y, iea[subgrid_to_index(grid, defaultpixel, x, y)])
      end
    end
    defaultpixel = (defaultpixel == 0) ? iea[0] : iea[0x1f]
    grid = newgrid
    logger.debug("Step #{step}:]n#{grid}");
  end

  # count number of lit pixels
  puts("After #{nsteps} enhancements, #{grid.sum_subgrid} lit pixels");
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
