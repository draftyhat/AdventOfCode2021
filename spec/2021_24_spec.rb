Inputfile = File.join(File.dirname(__FILE__), '..', 'input', '2021_24_input')
require "rspec/autorun"

require_relative '../2021_24_try2'

class MonadProcessor
  attr_reader :regs

  def initialize(input)
    @regs = { 'w'=>0, 'x'=>0,'y'=>0,'z'=>0 }
    @input = input.split('').map(&:to_i)
  end

  def get_value(arg)
    (@regs.include? arg) ? @regs[arg] : arg.to_i
  end

  def step(instruction)
    # parse instruction
    operator, arg0, arg1 = instruction.strip.split(' ')
    case operator
    when "inp"
      regs[arg0] = @input.shift
    when "add"
      regs[arg0] += get_value(arg1)
    when "mul"
      regs[arg0] *= get_value(arg1)
    when "mod"
      regs[arg0] = regs[arg0] % get_value(arg1)
    when "div"
      regs[arg0] = regs[arg0].div(get_value(arg1))
    when "eql"
      regs[arg0] = get_value(arg1) == regs[arg0] ? 1 : 0
    end
  end
end


describe "test run_section" do
  section_template = "inp w
mul x 0
add x z
mod x 26
div z %{s0}
add x %{s1}
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y %{s2}
mul y x
add z y"

  Sections.each do |section|
    sectiontext = section_template % { :s0 => section[0],
                                       :s1 => section[1],
                                       :s2 => section[2]  }

    (1..9).each do |input|
      [-13*26,13*26, 0, 1, -1, -10, 10, 13, -13, 25, -25, 26, -26, 27, -27].each do
        it "Checking run_section #{section[0]}, #{section[1]}, #{section[2]} input #{input}" do
          mp = MonadProcessor.new(input.to_s)
          sectiontext.each_line do |line|
            mp.step(line)
          end
          expect(run_section(input, 0, section[0], section[1], section[2])).to eq mp.regs['z']
        end
      end
    end
  end
end

