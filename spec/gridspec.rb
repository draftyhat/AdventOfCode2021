require "rspec/autorun"
require_relative "../lib/grid"
require "stringio"

describe Grid do
  context "Testing the Grid class" do
    it "Grid initialized with one element should have width 1, height 1" do
      rawgrid = StringIO.new("1")
      grid = Grid.new(fh: rawgrid)
      expect(grid.width).to eq 1
      expect(grid.height).to eq 1
      expect(grid.to_s == rawgrid)
    end

    it "2x3 Grid should have width 2, height 3" do
      rawgrid = StringIO.new("10 11\n20 21\n30 31")
      grid = Grid.new(fh: rawgrid)
      expect(grid.width).to eq 2
      expect(grid.height).to eq 3
      expect(grid.to_s == rawgrid)
    end

    it "2x3 single character Grid should have width 2, height 3" do
      rawgrid = StringIO.new("11\n22\n33")
      grid = Grid.new(fh: rawgrid, single_character: true)
      expect(grid.width).to eq 2
      expect(grid.height).to eq 3
      expect(grid.to_s == rawgrid)
    end

    rawgrid = StringIO.new("01234\n12345\n23456\n34567\n45678")
    grid = Grid.new(fh: rawgrid, single_character: true)
    rawgrid = StringIO.new("01234\n12345\n23456\n34567\n45678")
    grid_wrapped = Grid.new(fh: rawgrid, single_character: true, wrap: true)
    it "grid.get tests" do
      expect(grid.get(0,0)).to eq 0
      expect(grid.get(1,0)).to eq 1
      expect(grid.get(0,1)).to eq 1
      expect(grid.get(1,1)).to eq 2
      expect(grid.get(4,0)).to eq 4
      expect(grid.get(4,3)).to eq 7
      expect(grid.get(4,4)).to eq 8
    end

    it "out of bounds grid.get tests raise an exception" do
      expect { grid.get(-1,0) }.to raise_error(GridBoundaryError)
      expect { grid.get(0,-1) }.to raise_error(GridBoundaryError)
      expect { grid.get(-1,-1) }.to raise_error(GridBoundaryError)
      expect { grid.get(5,0) }.to raise_error(GridBoundaryError)
      expect { grid.get(0,5) }.to raise_error(GridBoundaryError)
      expect { grid.get(5,5) }.to raise_error(GridBoundaryError)
    end

    it "grid.get tests with default value" do
      expect(grid.get(0,0,default: 9)).to eq 0
      expect(grid.get(-1,0,default: 9)).to eq 9
      expect(grid.get(0,-1,default: 9)).to eq 9
      expect(grid.get(-1,-1,default: 9)).to eq 9
      expect(grid.get(0,5,default: 9)).to eq 9
      expect(grid.get(5,0,default: 9)).to eq 9
      expect(grid.get(5,5,default: 9)).to eq 9
    end

    it "Moving right operates correctly" do
      expect(grid.right(0,0)).to eq [1,0,1]
      expect(grid.right(0,1)).to eq [1,1,2]
      expect { grid.right(4,0) }.to raise_error(GridBoundaryError)
      expect { grid.right(5,0) }.to raise_error(GridBoundaryError)
      expect { grid.right(0,5) }.to raise_error(GridBoundaryError)
    end
    it "Moving right in wrapped grid operates correctly" do
      expect(grid_wrapped.right(0,0)).to eq [1,0,1]
      expect(grid_wrapped.right(0,1)).to eq [1,1,2]
      expect(grid_wrapped.right(4,0)).to eq [0,0,0]
    end
    it "Moving left operates correctly" do
      expect(grid.left(4,0)).to eq [3,0,3]
      expect(grid.left(3,1)).to eq [2,1,3]
      expect { grid.left(0,0) }.to raise_error(GridBoundaryError)
      expect { grid.left(-1,0) }.to raise_error(GridBoundaryError)
      expect { grid.left(0,5) }.to raise_error(GridBoundaryError)
    end
    it "Moving left in wrapped grid operates correctly" do
      expect(grid_wrapped.left(4,0)).to eq [3,0,3]
      expect(grid_wrapped.left(3,1)).to eq [2,1,3]
      expect(grid_wrapped.left(0,0)).to eq [4,0,4]
    end
    it "Moving up operates correctly" do
      expect(grid.up(0,1)).to eq [0,0,0]
      expect(grid.up(1,2)).to eq [1,1,2]
      expect { grid.up(0,0) }.to raise_error(GridBoundaryError)
      expect { grid.up(0,-1) }.to raise_error(GridBoundaryError)
      expect { grid.up(5,4) }.to raise_error(GridBoundaryError)
    end
    it "Moving up in wrapped grid operates correctly" do
      expect(grid_wrapped.up(0,1)).to eq [0,0,0]
      expect(grid_wrapped.up(1,2)).to eq [1,1,2]
      expect(grid_wrapped.up(0,0)).to eq [0,4,4]
    end
    it "Moving down operates correctly" do
      expect(grid.down(0,1)).to eq [0,2,2]
      expect(grid.down(1,2)).to eq [1,3,4]
      expect { grid.down(0,4) }.to raise_error(GridBoundaryError)
      expect { grid.down(-1,0) }.to raise_error(GridBoundaryError)
      expect { grid.down(5,4) }.to raise_error(GridBoundaryError)
    end
    it "Moving down in wrapped grid operates correctly" do
      expect(grid_wrapped.down(0,1)).to eq [0,2,2]
      expect(grid_wrapped.down(1,2)).to eq [1,3,4]
      expect(grid_wrapped.down(0,4)).to eq [0,0,0]
    end

    it "Checking grid sum" do
      expect(grid.sum_subgrid).to eq 100
      expect(grid.sum_subgrid(xmax:2,ymax:2)).to eq 4
      expect(grid.sum_subgrid).to eq 100
    end

    it "Checking grid resize" do
      rawgrid = StringIO.new("01234\n12345\n23456\n34567\n45678")
      grid = Grid.new(fh: rawgrid, single_character: true)
      grid.resize!(6, 6, default: 9)
      expect(grid.width).to eq 6
      expect(grid.height).to eq 6
      expect(grid.get(5,5)).to eq 9
    end

    it "Checking grid subgrid with recenter" do
      rawgrid = StringIO.new("01234\n12345\n23456\n34567\n45678")
      grid = Grid.new(fh: rawgrid, single_character: true)
      grid.resize!(3, 3, newx0:1, newy0:1, default: 9)
      expect(grid.get(0,0)).to eq 9
      expect(grid.get(0,1)).to eq 9
      expect(grid.get(1,0)).to eq 9
      expect(grid.get(1,1)).to eq 0
      expect(grid.get(2,2)).to eq 2
    end

    it "Checking rectangular subgrid" do
      rawgrid = StringIO.new("01234\n12345\n23456\n34567")
      grid = Grid.new(fh: rawgrid, single_character: true)
      grid.resize!(8, 6, newx0:1, newy0:1, default: 9)
      expect(grid.get(0,0)).to eq 9
      expect(grid.get(0,1)).to eq 9
      expect(grid.get(1,0)).to eq 9
      expect(grid.get(1,1)).to eq 0
      expect(grid.get(2,2)).to eq 2
      expect(grid.get(1,4)).to eq 3
      expect(grid.get(1,5)).to eq 9
      expect(grid.get(1,6,default:11)).to eq 11
      expect(grid.get(5,1)).to eq 4
      expect(grid.get(6,1)).to eq 9
      expect(grid.get(7,1)).to eq 9
      expect(grid.get(8,1,default:11)).to eq 11
    end

    it "Checking rectangular subgrid" do
      rawgrid = StringIO.new("01234\n12345\n23456\n34567")
      grid = Grid.new(fh: rawgrid, single_character: true)
      grid.resize!(6, 8, newx0:1, newy0:1, default: 9)
      expect(grid.get(0,0)).to eq 9
      expect(grid.get(0,1)).to eq 9
      expect(grid.get(1,0)).to eq 9
      expect(grid.get(1,1)).to eq 0
      expect(grid.get(2,2)).to eq 2
      expect(grid.get(4,1)).to eq 3
      expect(grid.get(5,1)).to eq 4
      expect(grid.get(6,1,default:11)).to eq 11
      expect(grid.get(1,4)).to eq 3
      expect(grid.get(1,5)).to eq 9
      expect(grid.get(1,6)).to eq 9
      expect(grid.get(1,7)).to eq 9
      expect(grid.get(1,8,default:11)).to eq 11
    end

    it "Checking grid translation" do
      rawgrid = StringIO.new("abcde\nbcdef\ncdefg\ndefgh\nefgh8")
      grid = Grid.new(fh: rawgrid, single_character: true,
                     translation_pattern: /[abcdefgh]/,
                     translation_map: { 'a'=>0,'b'=>1,'c'=>2,'d'=>3,'e'=>4,'f'=>5,'g'=>6,'h'=>7})
      expect(grid.get(0,0)).to eq 0
      expect(grid.get(1,0)).to eq 1
      expect(grid.get(0,1)).to eq 1
      expect(grid.get(1,1)).to eq 2
      expect(grid.get(4,0)).to eq 4
      expect(grid.get(4,3)).to eq 7
      expect(grid.get(4,4)).to eq 8
      expect(grid.sum_subgrid).to eq 100
      expect(grid.sum_subgrid(xmax:2,ymax:2)).to eq 4
      expect(grid.sum_subgrid).to eq 100
    end
  end
end

