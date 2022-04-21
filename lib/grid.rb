# utility grid class

class GridBoundaryError < StandardError
end

class Grid
  # a simple 2-d grid class

  include Enumerable

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
      #   well, most of the problems don't actually work this way
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

  def to_s_subgrid(xmax: -1, ymax: -1)
    xmax = xmax == -1 ? width() : xmax
    ymax = ymax == -1 ? height() : ymax
    # print a subgrid
    retval = []
    @grid[0...ymax].each do |row|
      retval.append(row[0...xmax].join(@delimiter))
    end

    retval.join("\n");
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

  def each(&block)
    @grid[0...@grid.length].each do |row|
      @row.each(&block)
    end
  end

  def up(x, y)
    newx, newy = bordercheck(x, y-1)
    return [newx, newy, @grid[newy][newx]]
  end
  def down(x, y)
    newx, newy = bordercheck(x, y+1)
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

  def _default_sum_method(x, y)
    x + y
  end

  def resize!(newwidth, newheight, default: 0)
    # extend or shrink the grid to the new dimensions. Initialize new spots
    # with the value default.
    (0...@grid.length).each do |rowindex|
      if newwidth < width
        @grid[rowindex] = @grid[rowindex][(0...newwidth)]
      else
        @grid[rowindex] = @grid[rowindex] + ([default] * (newwidth - width))
      end
    end

    if newheight < height
      @grid = @grid[(0...newheight)]
    else
      (height...newheight).each do |y|
        @grid.append([default] * newwidth)
      end
    end
    puts("grid[0] length #{@grid[0].length}");
    puts("grid length #{@grid.length}");
  end

  def sum_subgrid(xmax:-1,ymax:-1, p: :_default_sum_method)
    xmax = xmax == -1 ? width() : xmax
    ymax = ymax == -1 ? height() : ymax

    # sum a subgrid
    retval = 0
    @grid[0...ymax].each do |row|
      retval += row[0...xmax].reduce(0) { |memo, x| memo = send(p, memo, x) }
    end

    retval
  end
end
