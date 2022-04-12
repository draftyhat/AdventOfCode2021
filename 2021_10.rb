require 'logger'

AOCDAY = 10
AOCYEAR = 2021

CorruptedCharacterScores = {
  ')' => 3,
  ']' => 57,
  '}' => 1197,
  '>' => 25137,
}
CharacterMatch = {
  ')' => '(',
  ']' => '[',
  '}' => '{',
  '>' => '<',
}
IncompleteCharacterScores = {
  '(' => 1,
  '[' => 2,
  '{' => 3,
  '<' => 4,
}

def score_incomplete(charstack)
  score = 0
  charstack.reverse.each do |ch|
    score *= 5
    score += IncompleteCharacterScores[ch]
  end
  score
end

def run(inputfile, logger, **kwargs)
  incomplete_scores = []

  # part 1: find corrupted lines
  score = 0;
  linenumber = 0
  File.open(inputfile).each_line do |line|
    logger.debug("Line: #{line.strip}");
    linenumber += 1
    charstack = []
    line.strip.each_char do |ch|
      matchchar = CharacterMatch[ch]
      logger.debug("  char #{ch} matchchar #{matchchar}");
      if matchchar.nil?
        # no matching character. Push this character on to the stack.
        charstack << ch
      else
        ch_to_match = charstack.pop
        logger.debug("char #{ch} matchchar #{matchchar} ch_to_match #{ch_to_match}");
        if matchchar != ch_to_match
          # syntax error. Score, and move to the next line.
          logger.debug("Found mismatched character '#{ch}' on line #{linenumber}");
          score += CorruptedCharacterScores[ch]
          charstack = []
          break
        end
      end
    end

    # if we've processed every character but there remain characters in the
    # stack, this line is incomplete. 
    if charstack.length > 0
      logger.debug("Found incomplete line #{linenumber}. Remaining to match: #{charstack.join('')}");
      incomplete_scores << score_incomplete(charstack)
    end
  end

  puts("Syntax error score: #{score}");

  logger.debug("Incomplete lines scores: #{incomplete_scores} (found #{incomplete_scores.length})")
  puts("Incomplete lines score: #{incomplete_scores.sort[incomplete_scores.length.div(2)]}")
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
