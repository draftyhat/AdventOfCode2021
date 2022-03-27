AOCDAY = 1
AOCYEAR = 2021

def run(inputfile, **kwargs)
  previous_depth,*rest_depths = File.readlines(inputfile).map(&:to_i);

  count = 0;
  rest_depths.each do |next_depth|
    count += (next_depth > previous_depth ? 1 : 0)
    previous_depth = next_depth;
  end

  puts("#{count} increases");
end

def run_part2(inputfile, **kwargs)
  depths = File.readlines(inputfile).map(&:to_i);

  # note that window[a] < window[a+1]? is equivalent to
  #   window[a][0] < window[a+1][-1]

  puts kwargs
  window_size = kwargs.include?(:part2) ? 3 : 1
  puts window_size
  previous_depths = depths[0...window_size]
  rest_depths = depths[window_size..-1]

  count = 0;
  rest_depths.each do |next_depth|
    count += (next_depth > previous_depths[0] ? 1 : 0)
    previous_depths.shift
    previous_depths << next_depth;
  end

  puts("#{count} increases");
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
    run_part2(inputfile, **options)
  end
end
