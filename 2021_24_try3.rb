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

  try 2, work from the end

  try 3, work forward. Go 

=end

def run_section(input, z, a, b, c)
  # run a single section of MONAD
  x = z % 26
  z = z.div(a)
  x = (x + b != input) ? 1 : 0
  puts("----- x #{x}")
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


def run(logger, **kwargs)
  zs = [[0, 0]]
  Sections.each_with_index do |section, step|
    a, b, c = section
    newzs = []
    if a == 1
      # input is unrestricted. Try them all.
      # output == 26z + w + C
      (0..9).each do |newinput|
        zs.each do |z, input|
          newzs.append([26 * z + newinput + c, input * 10 + newinput])
        end
      end
    else
      # a == 26
      # must have z % 26 + b == w
      #  if so, z -> z/26
      zs.each do |z, input|
        newinput = (z % 26) + b
        if 1 <= newinput and newinput <= 9
          newzs.append([z/26, input * 10 + newinput])
        end
      end
    end

    zs = newzs;
    puts("After step #{step}, have #{zs.length} zs");
  end

  # filter out all inputs that didn't generate 0
  zs.keep_if {|z| z[0] == 0}

  zs[0].sort! {|z0,z1| z0[0] <=> z1[0] }
  puts(" Min input: #{zs[0][1]}")
  puts(" Max input: #{zs[-1][1]}")
  puts(" #{zs.length} inputs")
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
  run(logger, **options)
end
