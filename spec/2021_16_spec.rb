require_relative "../2021_16"
require "rspec/autorun"


describe "The get_n_bits function" do
  context "Testing the get_n_bits function" do
    it "Checking get_n_bits" do
      expect(get_n_bits('35AC', [0, 0], 1)).to eq [[0, 1], 0]
      expect(get_n_bits('35AC', [0, 0], 3)).to eq [[0, 3], 1]
      expect(get_n_bits('35AC', [0, 0], 4)).to eq [[1, 0], 3]
      expect(get_n_bits('35AC', [0, 1], 3)).to eq [[1, 0], 3]
      expect(get_n_bits('35AC', [0, 3], 1)).to eq [[1, 0], 1]

      expect(get_n_bits('35AC', [1, 0], 1)).to eq [[1, 1], 0]
      expect(get_n_bits('35AC', [1, 0], 3)).to eq [[1, 3], 2]
      expect(get_n_bits('35AC', [1, 0], 4)).to eq [[2, 0], 5]
      expect(get_n_bits('35AC', [1, 1], 3)).to eq [[2, 0], 5]
      expect(get_n_bits('35AC', [1, 3], 1)).to eq [[2, 0], 1]

      expect(get_n_bits('35AC', [0, 0], 5)).to eq [[1, 1], 6]
      expect(get_n_bits('35AC', [0, 0], 7)).to eq [[1, 3], 0x35 >> 1]
      expect(get_n_bits('35AC', [0, 0], 8)).to eq [[2, 0], 0x35]
      expect(get_n_bits('35AC', [0, 1], 4)).to eq [[1, 1], 3 << 1]
      expect(get_n_bits('35AC', [0, 1], 5)).to eq [[1, 2], 3 << 2 | 1]
      expect(get_n_bits('35AC', [0, 1], 7)).to eq [[2, 0], 0x35]
      expect(get_n_bits('35AC', [0, 1], 8)).to eq [[2, 1], 0x35 << 1 | 1]
      expect(get_n_bits('35AC', [0, 3], 4)).to eq [[1, 3], (1 << 3) | (0x5 >> 1)]
      expect(get_n_bits('35AC', [0, 3], 5)).to eq [[2, 0], (1 << 4) | 0x5]
      expect(get_n_bits('35AC', [0, 3], 8)).to eq [[2, 3], (1 << 7) | (0x5A >> 1)]
      expect(get_n_bits('35AC', [0, 3], 9)).to eq [[3, 0], (1 << 8) | 0x5A]
      expect(get_n_bits('35AC', [0, 3], 10)).to eq [[3, 1], (1 << 9) | (0x5A << 1) | 1]
      expect(get_n_bits('35AC', [1, 0], 8)).to eq [[3, 0], 0x5A]
      expect(get_n_bits('35AC', [1, 0], 9)).to eq [[3, 1], (0x5A << 1) | 1]
      expect(get_n_bits('35AC', [1, 2], 1)).to eq [[1, 3], 0]
    end
  end
end
