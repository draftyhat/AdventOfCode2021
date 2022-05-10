require 'logger'
require 'set'
require_relative 'lib/grid'

# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

AOCDAY = 15
AOCYEAR = 2021

class Node
  attr_reader :visited
  attr_reader :x
  attr_reader :y
  attr_reader :risk
  attr_accessor :distance
  include Comparable

  def initialize(x, y, risk)
    @x = x
    @y = y
    @risk = risk.to_i
    @visited = false
    @distance = nil
  end

  def visit(grid)
    @visited = true
    # check each neighbor
    [ [ @x-1, @y ],
      [ @x, @y-1 ],
      [ @x, @y+1 ],
      [ @x+1, @y ] ].each do |x, y|
      begin
        neighbornode = grid.get(x, y)
        neighbornode.set_distance(@distance)
      rescue GridBoundaryError => err
      end
    end
  end

  def visited?
    @visited
  end

  def <=>(other)
    if other.distance.nil?
      if @distance.nil?
        answer = 0
      else
        answer = -1
      end
    elsif @distance.nil?
      answer = 1
    else
      answer = @distance <=> other.distance
    end
    answer
  end

  def set_distance(x)
    # set distance if it's lower than what we have now
    if @distance.nil?
      @distance = x + @risk
    else
      @distance = [@distance, x + @risk].min
    end
  end

  def to_s
    "<#{@x},#{@y} #{@risk} #{@distance} #{visited? ? 'v':'.'}>"
  end
end


def run(inputfile, logger, **kwargs)
  grid = nil
  File.open(inputfile) do |fh|
    grid = Grid.new(fh: fh, single_character: true)
  end

  # create part 2 grid, 5x5 tiling
  if kwargs.include? :part2
    width = grid.width;
    height = grid.height;
    grid.resize!(width * 5, height * 5, default: 0);
    (0...width).each do |x|
      (height...5*height).each do |y|
        grid.set(x, y, (grid.get(x, y % height) + y.div(height) - 1) % 9 + 1)
      end
    end
    (width...5*width).each do |x|
      (0...5*height).each do |y|
        grid.set(x, y, (grid.get(x % width, y % height) + x.div(width) + y.div(height) - 1) % 9 + 1)
      end
    end
  end

  # Djikstra
  # Ruby doesn't seem to have a sorted list (like heapq), so we try re-sorting,
  # see if that's efficient enough.

  # convert each grid square to a node. Also, add each node to the unvisited
  # set.
  unvisited = []
  (0...grid.width).each do |x|
    (0...grid.height).each do |y|
      newnode = Node.new(x, y, grid.get(x, y))
      grid.set(x, y, newnode)
      unvisited.append(newnode)
    end
  end

  # start by visiting (0,0)
  nextnode = unvisited.shift
  nextnode.distance = 0;
  nextnode.visit(grid)

  # on each iteration, visit the unvisited node with the smallest distance
  step=0
  while unvisited.length > 0
    unvisited.sort!
    nextnode = unvisited.shift

    # visit this node
    nextnode.visit(grid)

    # if this is the last node, print results
    if nextnode.x == grid.width - 1 and nextnode.y == grid.height - 1
      puts("Cheapest path #{nextnode.distance}")
      break
    end

    step += 1
    if step % 1000 == 0
      logger.debug("at step #{step}, #{unvisited.length} nodes left");
    end
  end

  # print out the final grid
  (0...grid.width).each do |x|
    (0...grid.height).each do |y|
      puts("(#{x},#{y}): #{grid.get(x,y)}");
    end
  end

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
