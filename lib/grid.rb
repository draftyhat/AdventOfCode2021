# utility grid class

class GridBoundaryError < StandardError
end

class Grid
  # a simple 2-d grid class

  include Enumerable

  def initialize(fh: nil, delimiter: ' ', single_character: false,
                 translation_pattern: nil, translation_map: nil,
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
        nextline = line.strip
        if not translation_pattern.nil?
          line.gsub!(translation_pattern, translation_map)
        end
        line.split(@delimiter).map(&:to_i)
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

  def to_s_subgrid(xmin: 0, ymin: 0, xmax: -1, ymax: -1)
    if xmax < 0
      xmax = height + xmax
    else
      xmax = [xmax, height].min
    end
    if ymax < 0
      ymax = height + ymax
    else
      ymax = [ymax, height].min
    end

    # print a subgrid
    retval = []
    @grid[ymin...ymax].each do |row|
      retval.append(row[xmin...xmax].join(@delimiter))
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

  def resize!(newwidth, newheight, newx0:0, newy0:0, default: 0)
    # extend or shrink the grid to the new dimensions. Initialize new spots
    # with the value default.
    #  dimensions of the square we keep from the old grid
    if newx0 < 0
      raise GridBoundaryError, "resizing grid origin to negative coordinate not currently supported"
    end
    if newy0 < 0
      raise GridBoundaryError, "resizing grid origin to negative coordinate not currently supported"
    end

    keepx = [width, newwidth - newx0].min
    keepy = [height, newheight - newy0].min
    newgrid = []

    #  initialize newgrid with 0...newy0 rows of default, width newwidth
    (0...newy0).each do |y|
      newgrid << [default] * newwidth
    end

    #  copy overlapping square from oldgrid to newgrid. Also, extend to
    #  newwidth by prepending newx0 default values, and appending default values
    #  to extend width to newwidth
    #  cross-section:
    #     |   default   |   oldgrid     |     default    |
    #     0            newx0      newx0 + keepx       newwidth
    appendwidth = [0, newwidth - (newx0 + keepx)].max
    (0...keepy).each do |rowindex|
      newgrid << [default] * newx0 \
        + @grid[rowindex].slice(0, keepx) \
        + [default] * appendwidth;
    end

    # initialize leftovers from maxy to newheight with default
    (keepy + newy0...newheight).each do
      newgrid << [default] * newwidth
    end

    @grid = newgrid
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
