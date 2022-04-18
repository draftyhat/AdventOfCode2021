# utility grid class

class GridBoundaryError < StandardError
end

class Grid
  # a simple grid class
  #  bottom left is 0,0 by default (so, Cartesian-ish); y increases the row
  #  number, and x increases the column number

  def initialize(fh: nil, delimiter: ' ', single_character: false,
                 width: 0, height: 0, default: 0,
                 wrap: false, infiniteborder: false)
    # initialize from file read:
    # initialize the grid by reading fh, line by line, with elements of the class
    # initializer separated by the delimiter
    #  single_character: grid elements contain a single character
    # OR, initialize the grid with given width and height using a default value
    #  wrap: when falling off one edge of the grid, teleport to the other side
    #  infiniteborder: never fall off one edge of the grid, just remain on the border
    done = false
    @width = 0
    local_grid = []
    @wrap = wrap
    @delimiter = delimiter

    if single_character
      @delimiter = ''
    end

    if not fh.nil?
      fh.readlines.each do |line|
        nextline = line.strip.split(@delimiter).map(&:to_i)
        if nextline.length > 0
          local_grid << nextline
        else
          done = true
        end
      end

      # make 0,0 bottom left
      #@grid = local_grid.reverse;
      @grid = local_grid
      
    else
      # initialize grid based on height, width
      @grid = []
      (0...height).each do |y|
        @grid.append([default]*width)
      end
    end
  end

  def to_s()
    retval = ''
    @grid.each do |row|
      retval += row.join(@delimiter)
      retval += "\n"
    end
    return retval;
  end
    
  def width()
    return @grid[0].length
  end
  def height()
    return @grid.length
  end
  def bordercheck(x, y)
    if @wrap
      x = x % @grid[0].length
      y = y % @grid.length
    elsif @infiniteborder
      x = (x < 0)? 0 : ((x >= @grid[0].length) ? @grid[0].length : x)
      y = (y < 0)? 0 : ((y >= @grid.length) ? @grid.length : y)
    elsif x < 0 or x >= @grid[0].length or y < 0 or y >= @grid.length
      raise GridBoundaryError.new("Point #{x}, #{y} exceeds grid dimensions" \
                              " #{@grid[0].length}, #{@grid.length}")
    end

    return [x, y]
  end

  def get(x, y, default: nil)
    begin
      x, y = bordercheck(x, y)
      return @grid[y][x]
    rescue GridBoundaryError => err
      if not default.nil?
        return default
      else
        raise err
      end
    end
  end
  def set(x, y, value)
    @grid[y][x] = value;
  end

  def up(x, y)
    newx, newy = bordercheck(x, y+1)
    return [newx, newy, @grid[newy][newx]]
  end
  def down(x, y)
    newx, newy = bordercheck(x, y-1)
    return [newx, newy, @grid[newy][newx]]
  end
  def left(x,y)
    newx, newy = bordercheck(x-1, y)
    return [newx, newy, @grid[newy][newx]]
  end
  def right(x,y)
    newx, newy = bordercheck(x+1, y)
    return [newx, newy, @grid[newy][newx]]
  end
end
