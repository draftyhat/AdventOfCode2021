require 'logger'
require 'scanf'

AOCDAY = 17
AOCYEAR = 2021

def step(x, y, v_x, v_y)
  # moves probe one step. Returns the arguments.
  new_v_x = v_x > 0 ? v_x - 1 : 0
  return [x + v_x, y + v_y, new_v_x, v_y - 1]
end

def in_target(x, y, targetbounds)
  xmin, xmax, ymin, ymax = targetbounds
  x >= xmin and x <= xmax and y >= ymin and y <= ymax
end

def exceeds_target?(x, y, targetbounds)
  xmin, xmax, ymin, ymax = targetbounds
  x > xmax or y < ymin
end

def shoot(v_x, v_y, targetbounds, logger)
  logger.debug(" --- shooting #{v_x},#{v_y}")
  # iterate steps until we're out
  x, y, v_x_local, v_y_local = [0, 0, v_x, v_y]
  maxheight = 0
  while not exceeds_target?(x, y, targetbounds)
    logger.debug(" #{v_x},#{v_y}: (#{x},#{y})  v #{v_x_local},#{v_y_local}")
    x, y, v_x_local, v_y_local = step(x, y, v_x_local, v_y_local)
    maxheight = [maxheight, y].max
    if in_target(x, y, targetbounds)
      return [v_x, v_y, maxheight]
    end
  end
  return nil
end

def run(inputfile, logger, **kwargs)
  targetbounds = []
  File.open(inputfile) do |fh|
    targetbounds = fh.readline.strip.scanf('target area: x=%d..%d, y=%d..%d');
  end
  xmin, xmax, ymin, ymax = targetbounds

  # answers will be an array of [v_x, v_y, greatest_height]
  answers = []
  (1..xmax).each do |v_x|
    ymaxabs = [ymax.abs, ymin.abs].max
    (-ymaxabs..ymaxabs).each do |v_y|
      answer = shoot(v_x, v_y, targetbounds, logger)
      if not answer.nil?
        answers << answer
      end
    end
  end

  # find the highest probe height
  answers.sort! { |a, b| a[2] <=> b[2] }
  puts("Highest probe height #{answers[-1][2]}")
  puts("Number of target-catching velocities #{answers.length}")
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
