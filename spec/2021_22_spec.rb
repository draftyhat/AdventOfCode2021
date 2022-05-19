# cube unions
require "rspec/autorun"
require_relative "../2021_22"

describe Cube do
  context "Test cube size routine" do
    it "off cube should get size 0" do
      cube = Cube.new("off x=1..1,y=2..2,z=3..3")
      expect(cube.size).to eq 0
    end
    it "off cube should get size 0" do
      cube = Cube.new("off x=1..1,y=2..4,z=3..3")
      expect(cube.size).to eq 0
    end
    it "off cube should get size 0" do
      cube = Cube.new("off x=1..1,y=2..2,z=3..6")
      expect(cube.size).to eq 0
    end

    it "1x1x1 cube should get size 1" do
      cube = Cube.new("on x=1..1,y=2..2,z=3..3")
      expect(cube.size).to eq 1
    end
    it "2x2x2 cube should get size 8" do
      cube = Cube.new("on x=-1..0,y=2..3,z=3..4")
      expect(cube.size).to eq 8
    end
    it "3x3x3 cube should get size 27" do
      cube = Cube.new("on x=1..3,y=-2..0,z=3..5")
      expect(cube.size).to eq 27
    end
    it "3x3x3 cube (with negative coords should get size 27" do
      cube = Cube.new("on x=1..3,y=-1..1,z=3..5")
      expect(cube.size).to eq 27
    end
    it "1x1x2 cube should get size 2" do
      cube = Cube.new("on x=1..1,y=2..2,z=-3..-2")
      expect(cube.size).to eq 2
    end
    it "1x2x1 cube should get size 2" do
      cube = Cube.new("on x=1..1,y=2..3,z=3..3")
      expect(cube.size).to eq 2
    end
    it "2x1x1 cube should get size 2" do
      cube = Cube.new("on x=-2..-3,y=2..2,z=3..3")
      expect(cube.size).to eq 2
    end
    it "1x2x2 cube should get size 4" do
      cube = Cube.new("on x=1..1,y=2..3,z=3..4")
      expect(cube.size).to eq 4
    end
  end
  context "Test cube intersect routine" do
    it "bordering cubes should intersect" do
      cube0 = Cube.new("on x=0..1,y=2..3,z=3..4")
      cube1 = Cube.new("on x=1..2,y=1..4,z=2..6")
      expect(cube0.intersects?(cube1)).to eq true
    end
    it "completely contained cube should intersect" do
      cube0 = Cube.new("on x=1..1,y=2..3,z=3..4")
      cube1 = Cube.new("on x=0..2,y=1..4,z=2..6")
      expect(cube0.intersects?(cube1)).to eq true
    end
    it "completely contained cube should intersect" do
      cube0 = Cube.new("on x=1..1,y=2..3,z=3..4")
      cube1 = Cube.new("on x=0..2,y=1..4,z=2..6")
      expect(cube0.intersects?(cube1)).to eq true
    end
  end
  context "Test cube union routine" do
  end
end
