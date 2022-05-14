require 'logger'

AOCDAY = 18
AOCYEAR = 2021

$logger = Logger.new(STDOUT);

class SnailfishNumber
  attr_accessor :lhs
  attr_accessor :rhs
  attr_accessor :parent
  def initialize(s, parent: nil)
    @lhs, @rhs = s
    @parent = parent

    if @lhs.class == SnailfishNumber
      @lhs.parent = self
    elsif @lhs.class == Array
      @lhs = SnailfishNumber.new(@lhs, parent: self)
    end
    if @rhs.class == SnailfishNumber
      @rhs.parent = self
    elsif @rhs.class == Array
      @rhs = SnailfishNumber.new(@rhs, parent: self)
    end
    $logger.debug("-- init #{self} parent #{parent}")
  end

  def clone()
    SnailfishNumber.new([@lhs.clone, @rhs.clone])
  end

  def explode?(depth)
    # returns true if did explode
    retval = false
    if @lhs.class == SnailfishNumber
      retval = @lhs.explode?(depth + 1)
    end
    if not retval and (@rhs.class == SnailfishNumber)
      retval = @rhs.explode?(depth + 1)
    end
    if not retval and depth >=4 and @lhs.class == Integer and @rhs.class == Integer
      # bottom-level pair; explode this
      retval = true

      # search back up for next lhs number
      searchee = self
      $logger.debug("EXPLODE start, #{searchee}");
      while not searchee.nil?
        # if we're the lhs of our parent, keep searching up
        if not searchee.parent.nil?
          $logger.debug("LHS: searchee #{searchee} parent #{searchee.parent} lhs? #{searchee.parent.lhs == searchee}")
        end
        if searchee.parent.nil? or searchee.parent.lhs == searchee
          # move up
          searchee = searchee.parent;
          $logger.debug("LHS: navigated up, searchee now #{searchee}")
        else
          # move down
          # else we're the rhs of our parent. Take the lhs; search to the
          # rightmost element; add to that number.
          searchee = searchee.parent
          if searchee.lhs.class == Integer
            $logger.debug("LHS: found next lhs, searchee #{searchee}")
            searchee.lhs += @lhs
            searchee = nil
            $logger.debug("LHS: found next lhs, altered to #{searchee}");
          else
            $logger.debug("LHS: we were the rhs of #{searchee}, now searching right down #{searchee.lhs}")
            searchee = searchee.lhs
            while searchee.rhs.class != Integer
              searchee = searchee.rhs
              $logger.debug("LHS:  searching right down #{searchee}")
            end
            searchee.rhs += @lhs
            $logger.debug("LHS: found next rhs, altered to #{searchee}");
            searchee = nil
          end
        end
      end

      # search back up for next rhs number
      searchee = self
      $logger.debug("EXPLODE RHS start, #{searchee}");
      while not searchee.nil?
        # if we're the rhs of our parent, keep searching up
        if not searchee.parent.nil?
          $logger.debug("RHS: searchee #{searchee} parent #{searchee.parent} rhs? #{searchee.parent.rhs == searchee}")
        end
        if searchee.parent.nil? or searchee.parent.rhs == searchee
          # move up
          searchee = searchee.parent;
          $logger.debug("RHS: navigated up, searchee now #{searchee}")
        else
          # move down
          # else we're the lhs of our parent. Take the rhs; search to the
          # leftmost element; add to that number.
          searchee = searchee.parent
          if searchee.rhs.class == Integer
            $logger.debug("RHS: found next rhs, searchee #{searchee}")
            searchee.rhs += @rhs
            searchee = nil
            $logger.debug("RHS: found next rhs, altered to #{searchee}");
          else
            $logger.debug("RHS: we were the lhs of #{searchee}, now searching left down #{searchee.rhs}")
            searchee = searchee.rhs
            while searchee.lhs.class != Integer
              searchee = searchee.lhs
              $logger.debug("RHS:  searching left down #{searchee}")
            end
            searchee.lhs += @rhs
            $logger.debug("RHS: found next lhs, altered to #{searchee}");
            searchee = nil
          end
        end
      end

      # replace this instance with 0 in the parent
      if (@parent.rhs == self)
        @parent.rhs = 0
      else
        @parent.lhs = 0
      end
    end
    return retval
  end

  def split?()
    # check for splits: perform the first split
    # return true if split
    retval = false
    if @lhs.class == Integer
      if @lhs >= 10
        # do split
        @lhs = SnailfishNumber.new([@lhs.div(2), (@lhs + 1).div(2)], parent: self)
        retval = true
      end
    else
      # lhs is not an integer; must be a SnailfishNumber
      retval = @lhs.split?
    end

    if not retval
      # same thing on the rhs
      if @rhs.class == Integer
        if @rhs >= 10
          @rhs = SnailfishNumber.new([@rhs.div(2), (@rhs + 1).div(2)], parent: self)
          retval = true
        end
      else
        # rhs is a SnailfishNumber
        retval = @rhs.split?
      end
    end

    return retval
  end

  def snail_reduce!()
    $logger.debug("reducing #{self}")
    # reduce this number
    didsomething = true
    while didsomething
      didsomething = explode?(0)
      if not didsomething
        didsomething = split?
        if didsomething
          $logger.debug(" after split:   #{self}")
        end
      else
        $logger.debug(" after explode: #{self}")
      end
    end
  end

  def add(n)
    # add in a new snailfish number
    # returns a new snailfish number
    x = SnailfishNumber.new([self, n])
    x.snail_reduce!
    return x
  end

  def to_s()
    return "[#{@lhs.to_s},#{@rhs.to_s}]"
  end

  def magnitude()
    lvalue = @lhs
    if SnailfishNumber == @lhs.class
      lvalue = @lhs.magnitude
    end
    rvalue = @rhs
    if SnailfishNumber == @rhs.class
      rvalue = @rhs.magnitude
    end

    #$logger.debug("----- #{3*lvalue + 2*rvalue} from l #{lvalue} r #{rvalue} from #{self}")
    3*lvalue + 2*rvalue
  end
end

#x = SnailfishNumber.new([[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]])
#y = SnailfishNumber.new([[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]])
#puts("adding #{x} to #{y}")
#z = x.add(y)
#puts("  #{z}")
#puts("Mag #{z.magnitude}")
#
#z = SnailfishNumber.new([[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]])
#puts("  #{z}")
#puts("Mag #{z.magnitude}")
#raise NoSuchError


def run(inputfile, **kwargs)
  numbers = []
  File.open(inputfile).each_line do |line|
    numbers << SnailfishNumber.new(eval(line.strip))
  end

  max_magnitude = 0
  if kwargs.include?(:part2)
    # find the larges magnitude of the sum of any two numbers
    numbers.permutation(2).each do |x,y|
      xp = x.clone
      yp = y.clone
      zp = xp.add(yp)
      new_magnitude = zp.magnitude
      max_magnitude = [max_magnitude, new_magnitude].max
    end
    puts("Max pair magnitude #{max_magnitude}")
  else
    n = numbers.reduce(:add)
    puts("Final snailfish number: #{n}")
    puts("Final magnitude: #{n.magnitude}")
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

  $logger.level = (options.include? :verbose) ? Logger::DEBUG : Logger::WARN

  ARGV.each do |inputfile|
    run(inputfile, **options)
  end
end
