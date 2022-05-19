require 'logger'
require 'scanf'

AOCDAY = 22
AOCYEAR = 2021

class Cube
  attr_accessor :xmin, :xmax, :ymin, :ymax, :zmin, :zmax, :on

  def initialize(line)
    onstr,xmin,xmax,ymin,ymax,zmin,zmax = line.scanf("%s x=%d..%d,y=%d..%d,z=%d..%d")
    @xmin = [xmin, xmax].min
    @xmax = [xmin, xmax].max
    @ymin = [ymin, ymax].min
    @ymax = [ymin, ymax].max
    @zmin = [zmin, zmax].min
    @zmax = [zmin, zmax].max
    @on = (onstr == 'on') ? true : false
  end

  def size()
    retval = 0
    if @on
      retval = (@xmax + 1 - @xmin) * (@ymax + 1 - @ymin) * (@zmax + 1 - @zmin)
    end
    retval
  end

  def intersects?(other)
    # does this cube intersect the other cube?
    if @xmax < other.xmin or @xmin > other.xmax \
        or @ymax < other.ymin or @ymin > other.ymax \
        or @zmax < other.zmin or @zmin > other.zmax
      return false
    end
    return true
  end

  def intersection(other)
    # return the cube delineating the intersection of this cube and the other
    # cube.
    # we assume other intersects with us
    #  on a number line:
    #     xmin0----xmin1---xmax0----xmax1
    #                   OR
    #     xmin0----xmin1---xmax1----xmax0
    #                   OR
    #     xmin1----xmin0---xmax0----xmax1
    #                   OR
    #     xmin1----xmin0---xmax1----xmax0
    # so the intersection is [xmin0,xmin1].max .. [xmax0,xmin1].min
    # and that extrapolates to 3 dimensions
    return Cube.new("on x=#{[@xmin,other.xmin].max}..#{[@xmax,other.xmax].min}," \
                       "y=#{[@ymin,other.ymin].max}..#{[@ymax,other.ymax].min}," \
                       "z=#{[@zmin,other.zmin].max}..#{[@zmax,other.zmax].min}")
  end

  def to_s()
    puts("#{@on? 'on':'off'} x=#{xmin}..#{xmax},y=#{ymin}..#{ymax},z=#{zmin}..#{zmax}")
  end

  def to_cubes()
    retval = []
    (xmin..xmax).each do |x|
      (ymin..ymax).each do |y|
        (zmin..zmax).each do |z|
          retval << [x,y,z]
        end
      end
    end
    retval
  end
end

def calculate_union_volume(input_cubes, logger)
  # reversing the order means we can treat OFF cubes and ON cubes identically.
  # When adding an OFF cube, we'll simply add it to the list, without doing any
  # overlap calculations on cubes preceding it in the list (cubes that would be
  # added after this cube, if we were working forward in time). We will include
  # overlap calculations on any subsequently-added cubes -- cubes that would
  # precede placement of the OFF cube if we were working forward in time. This
  # will effectively remove cubes that need to be turned off from the final
  # calculation.
  # (thanks reddit community for this trick!)
  input_cubes.reverse!

  cubes = []
  volume = 0
  input_cubes.each do |newcube|
    # if the cube is off, do nothing except add it to the list of cubes to track.
    if newcube.on
      # add the volume of this new cube
      newvolume = newcube.size

      # calculate all overlapping regions.
      overlaps = []
      cubes.each do |oldcube|
        if newcube.intersects?(oldcube)
          overlaps << newcube.intersection(oldcube)
        end
      end
      # use this routine to calculate the total volume of the overlaps. This
      # accounts for overlapping overlaps!
      overlapvolume = calculate_union_volume(overlaps, logger)

      # Subtract the volume of the overlaps from the new volume.
      newvolume -= overlapvolume

      # add in the volume we've just calculated
      volume += newvolume
    end
    cubes << newcube
  end

  # clean up our changes to our input argument
  input_cubes.reverse!

  volume
end
      

def run(inputfile, logger, **kwargs)
  input_cubes = []
  File.open(inputfile).each_line do |line|
    newcube = Cube.new(line.strip)

    # very cheap include-only-cubes-in-part1-range filter
    if kwargs.include? :part2 or (newcube.xmin >= -50 and newcube.xmin <= 50)
      input_cubes << newcube
    end
  end

  volume = calculate_union_volume(input_cubes, logger)
  puts("Final volume: #{volume} cubes")
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
