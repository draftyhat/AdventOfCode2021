require 'logger'

AOCDAY = 5
AOCYEAR = 2021

def run(inputfile, logger, **kwargs)
  points = []
  File.open(inputfile).each_line do |line|
    newvectors = line.split(' -> ')
    x0,y0 = newvectors[0].split(',').map(&:to_i);
    x1,y1 = newvectors[1].split(',').map(&:to_i);

    logger.debug("#{x0},#{y0} -> #{x1},#{y1}");

    if not kwargs.include? :part2
      # skip diagonals
      if not (x0 == x1) || (y0 == y1)
        next
      end
    end

    # add all points specified by this vector to our list
    #  size of the array is x1-x0 unless x0 == x1, use y1-y0
    size = [(x1-x0).abs, (y1-y0).abs].max + 1
    xarr = (x0 == x1) ? [x0]*size : (x0..x1).step(x1 > x0 ? 1 : -1)
    yarr = (y0 == y1) ? [y0]*size : (y0..y1).step(y1 > y0 ? 1 : -1)

    logger.debug("  adding new points #{xarr} + #{yarr} = #{xarr.zip(yarr)}")
    points += xarr.zip(yarr);
  end

  # Count points with > 1 occurences.
  logger.debug("----------");
  logger.debug(points.group_by {|i| i}.map{|k,v| [ v.count ]})
  logger.debug(points.group_by {|i| i}.map{|k,v| [ v.count > 1 ? 1:0]})
  answer = points.group_by {|i| i}.map{|k,v| [v.count > 1 ? 1:0]}.flatten.sum
  puts("Answer: #{answer}");
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
