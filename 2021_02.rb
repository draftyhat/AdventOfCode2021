AOCDAY = 2
AOCYEAR = 2021

def run(inputfile, **kwargs)
  depth = 0;
  horiz = 0;
  part2_aim = 0;
  part2_depth = 0;

  File.open(inputfile).each_line do |line|
    direction,amount = line.split(' ')
    amount = amount.to_i
    case direction
    when "forward"
      horiz += amount
      part2_depth += amount * part2_aim
    when "up"
      depth -= amount
      part2_aim -= amount
    when "down"
      depth += amount
      part2_aim += amount
    end
  end

  puts "Final position: #{horiz} down #{depth} gives #{horiz * depth}"
  puts "Final part2 position: #{horiz} down #{part2_depth} gives #{horiz * part2_depth}"
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


  ARGV.each do |inputfile|
    run(inputfile, **options)
  end
end
