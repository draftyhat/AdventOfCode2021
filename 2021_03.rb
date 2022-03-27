AOCDAY = 3
AOCYEAR = 2021

def run(inputfile, **kwargs)
  nlines = 0
  onebits = {}
  onebits.default = 0
  File.open(inputfile).each_line do |line|
    nlines += 1
    pos = 0;
    line.split("").each_with_index do |ch, idx|
      if '1' == ch
        onebits[idx] += 1;
      end
    end
  end

  # find most common bit, shift this into gamma
  # other bit is least common bit; shift this into epsilon
  gamma = 0;
  epsilon = 0;
  (0...onebits.length).each do |idx|
    gamma <<= 1
    epsilon <<= 1
    nfound = onebits[idx]
    if nfound > nlines/2
      gamma += 1
    else
      epsilon += 1
    end
  end

  puts "Power consumption: #{gamma * epsilon}"
end

def run_part2(inputfile, **kwargs)
  nlines = 0

  def most_common_bit(arr, idx, default = '1')
    onescount = 0;
    arr.each do |line|
      if line[idx] == '1'
        onescount += 1
      end
    end

    puts("--- onescount at #{idx}: #{onescount} (arr/2 #{arr.length}/2 #{arr.length/2})");
    if onescount * 2 >= arr.length
      return '1'
    end

    return '0'
  end

  co2lines = File.readlines(inputfile);

  o2lines = co2lines.clone()
  idx = 0
  while o2lines.length > 1
    commonbit = most_common_bit(o2lines, idx)
    o2lines = o2lines.select { |line| line[idx] == commonbit }
    idx += 1
  end
  o2gen = o2lines[0].to_i(2);

  idx = 0
  while co2lines.length > 1
    commonbit = most_common_bit(co2lines, idx)
    # flip commonbit
    commonbit = (commonbit == "1" ? "0" : "1")
    puts("----- position #{idx} least common #{commonbit}");
    co2lines = co2lines.select { |line| line[idx] == commonbit }
    puts(co2lines)
    idx += 1
  end
  co2scrub = co2lines[0].to_i(2);

  puts "Life support rating: #{o2gen} * #{co2scrub} = #{o2gen * co2scrub}"
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
    if options.include? :part2
      run_part2(inputfile, **options)
    else
      run(inputfile, **options)
    end
  end
end
