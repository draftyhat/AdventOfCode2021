require 'logger'
require_relative 'lib/grid'

AOCDAY = 11
AOCYEAR = 2021

def flash(grid)
  flashstack = []
  (0...grid.width).each do |x|
    (0...grid.height).each do |y|
      # increment energy level for this octopus
      energylevel = grid.get(x, y)
      grid.set(x, y, energylevel + 1)

      # push every octopus that needs to be flashed on the flashstack
      if energylevel >= 9
        flashstack << [x,y]
      end
    end
  end

  # pop each flashing octopus. Add any octopi this flash causes to flash
  # to the flashstack.
  flasher = flashstack.pop
  while not flasher.nil?
    x,y = flasher
    # increment the energy level of every octopus adjacent to this octopus
    [[x-1,y+1], [x,y+1], [x+1,y+1], [x-1,y], [x+1,y], [x-1,y-1], [x,y-1], [x+1,y-1]].each do |neighborx, neighbory|
      # if this is an octopus, increment its energy level
      begin
        energylevel = grid.get(neighborx,neighbory)
        grid.set(neighborx, neighbory, energylevel + 1)

        # if this octopus flashes, add it to the flashstack
        if 9 == energylevel
          flashstack << [neighborx, neighbory]
        end
      rescue GridBoundaryError => err
      end
    end
    flasher = flashstack.pop
  end

  # process all flashes (value 10 in the grid)
  nflashes = 0
  (0...grid.width).each do |x|
    (0...grid.height).each do |y|
      if grid.get(x,y) > 9
        nflashes += 1
        grid.set(x, y, 0)
      end
    end
  end

  # return number of flashes
  nflashes
end

def run(inputfile, logger, **kwargs)
  # read grid
  grid = Grid.new(fh: File.open(inputfile), single_character: true)

  flashcount = 0;
  nsteps = 0;
  
  flashcount_this_step = 0;
  # loop ends after all octopi have flashed together
  while flashcount_this_step != grid.width * grid.height
    # count flashes this step
    flashcount_this_step = flash(grid);

    # record total number of flashes in first 100 steps
    nsteps += 1;
    if nsteps <= 100
      flashcount += flashcount_this_step
    end
    if nsteps < 10
      logger.debug("Step #{nsteps}:\n#{grid.to_s}")
    end
  end

  puts("#{flashcount} flashes in 100 steps!");
  puts("All octopi flashed together at step #{nsteps}");
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
