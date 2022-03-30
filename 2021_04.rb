AOCDAY = 1
AOCYEAR = 2021

class Marked
  def to_i
    0
  end

  def to_s
    "__"
  end
end

class Board
  def initialize(fh, size = 5)
    @grid = []
    # read 5 lines
    (0...size).each do
      @grid << fh.readline().split(' ').map(&:to_i)
    end
  end

  def to_s
    rows = []
    @grid.each do |row|
      rows << (row.map {|x| x.to_s.rjust(2, '0')}).join(' ')
    end
    return rows.join("\n");
  end

  def column_marked(i)
    # is the ith column filled in?
    elements = @grid.transpose[i]
    selected = elements.select { |x| x.class == Marked }
    selected.length == elements.length
  end

  def row_marked(i)
    # is the ith row filled in?
    elements = @grid[i]
    selected = elements.select { |x| x.class == Marked }
    selected.length == elements.length
  end

  def nrows()
    return @grid.length
  end
  def ncolumns()
    return @grid[0].length
  end

  def mark(i)
    # mark an integer. Return true if bingo.
    # find the integer in the grid and replace it with Marked
    @grid.each_with_index do |row, rowindex|
      row.each_with_index do |element, columnindex|
        if element == i
          @grid[rowindex][columnindex] = Marked.new
          if row_marked(rowindex) or column_marked(columnindex)
            return true;
          end
          return false;
        end
      end
    end
    false
  end

  def guess(i)
    # returns true if bingo
    # mark i and check for bingo
    if self.mark(i)
      return score(i)
    end
    return 0;
  end

  def score(i)
    # score a board that's (assumed to be) complete
    # input: the last number marked
    score = 0
    @grid.each do |row|
      score += row.map(&:to_i).sum
    end
    #  sum all unmarked numbers
    #  multiply by last number
    i * score
  end

end

def run(inputfile, logger, **kwargs)
  begin
    fh = File.open(inputfile)

    # read guesses
    guesses = fh.readline.split(',').map(&:to_i)

    # read bingo cards
    boards = [];
    while fh.readline
      boards << Board.new(fh)
    end

  rescue EOFError => err

  ensure
    fh.close unless fh.nil?
  end

  guesses.each_with_index do |guess, guessindex|
    removethese = []
    boards.each_with_index do |board, boardindex|
      x = board.guess(guess)
      if x > 0
        puts("Board wins! Score #{x}");
        removethese << boardindex
      end
    end
    logger.debug("Deleting boards #{removethese}");
    removethese.reverse.each do |i|
      boards.delete_at(i)
    end
    logger.debug("#{boards.length} boards left");
  end
end


if __FILE__ == $0
  require 'optparse'
  require 'logger'

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
  logger.level = ((options.include? :verbose) ? Logger::WARN : Logger::INFO)

  ARGV.each do |inputfile|
    run(inputfile, logger, **options)
  end
end
