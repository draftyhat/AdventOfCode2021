require 'logger'

AOCDAY = 24
AOCYEAR = 2021

=begin
notes
  w = input
  x = z % 26
  z /= A  (A is 26 or 1)
  x += B
  w = (x == w)
  x = (x == 0)
  z *= 25x + 1  so this is either z*26 or z*1
  z = (w + C) * x


  x = (Z % 26) + A
  w = ((Z % 26) + A) == w
  x = ((Z % 26) + A) == 0


  w = input
  x = (z % 26) + B
  z /= A

  ok
  try 1, brute force (ish):
  z is the only # preserved between sections
  calculate all possible values of z for first section
  use crossproduct of values of z, values of 2nd digit to calculate all possible values of z for section section
  etc.

=end

def run_section(input, z, a, b, c)
  # run a single section of MONAD
  x = z % 26
  z = z.div(a)
  x = (x + b != input) ? 1 : 0
  z *= 25 * x + 1
  z += (input + c) * x
  z
end

Sections = [
  [1, 15, 15],
  [1, 12, 5],
  [1, 13, 6],
  [26, -14, 7],
  [1, 15, 9],
  [26, -7, 6],
  [1, 14, 14],
  [1, 15, 3],
  [1, 15, 1],
  [26, -7, 3],
  [26, -8, 4],
  [26, -7, 6],
  [26, -5, 7],
  [26, -10, 1],
]


def run_in_reverse(logger, **kwargs)
  # start with the zeros of the last section (that is, 0, with an empty input string)
  zeros = Hash.new{|h, k| h[k] = []}
  zeros[0] = ['']

  # taking the sections in reverse order
  Sections.reverse.each do |a,b,c|
    puts("Running section #{a},#{b},#{c}; starting with #{zeros.length} zeros")
    puts("   first 10 zeroes: #{zeros.keys.slice(0,10)}")
    logger.debug("Running section #{a},#{b},#{c}; starting with #{zeros.length} zeros")
    newzeros = Hash.new{|h, k| h[k] = []}

    # find the inputs that create a zero for this section
    # arbitrarily, assume that input z will always be between -13*26 and 13*26
    (-1325*26..1325*26).each do |z|
      (1..9).each do |inputdigit|
        newz = run_section(inputdigit, z, a, b, c)
        if zeros[newz].length > 0
          #logger.debug("  found new zero #{newz}, input digit #{inputdigit}")
          # add this to the zeros for this section
          newzeros[z] += zeros[newz].map {|x| inputdigit.to_s + x}
        end
      end
    end

    logger.debug(newzeros)
    zeros = newzeros
  end

  # output results
  puts("Zeroes:")
  zeros.each do |z, inputlist|
    inputlist.each do |input|
      puts("#{input}")
    end
  end

  # convert all inputs to integers and sort
  inputs = zeros.map {|key, valuelist| valuelist.map(&:to_i)}.flatten
  inputs.sort!
  puts("Found #{inputs.length} inputs. Max: #{inputs.max}")
end

def run(logger, **kwargs)
  zs = {0 => [0]}
  step = 0
  Sections.each_with_index do |triple, index|
    a, b, c = triple
    newzs = {}
    newzs.default = []
    (1..9).each do |inputdigit|
      zs.each do |z, inputs|
        logger.debug("Step #{step}, #{z}, inputdigit #{inputdigit}, #{a} #{b} #{c}, #{inputs.length} inputs")
        newz = run_section(inputdigit, a, b, c, z)
        newinputs = inputs.map {|x| x*10 + inputdigit}
        newzs[newz] += newinputs
      end
    end
    zs = newzs
    puts("Step 0: #{zs.length} zs")
    zs.each do |z, inputs|
      puts("  #{z}: #{inputs}")
    end
    step += 1
  end

  puts("Inputs that generate 0: #{zs[0]}")
  zs[0].sort!
  puts(" Max input: #{zs[0][-1]}")
  puts(" #{zs[0].length} inputs")
end


if __FILE__ == $0
  require 'optparse'

  options = {}
  OptionParser.new do |opts|
    opts.banner = "Usage: $0 [options]\n" \
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

  #run(logger, **options)
  run_in_reverse(logger, **options)
end
