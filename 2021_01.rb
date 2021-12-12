
increases=0;
last_depth = gets.to_i
depthlist = [last_depth]
while depthlist.length < 3 and line = gets
  next_depth = line.to_i
  if(next_depth > last_depth)
    puts("  increase!");
    increases += 1
  end
  last_depth = next_depth;
  depthlist.push(next_depth);
  puts(depthlist);
end

average_increases = 0;
while line = gets
  next_depth = line.to_i
  if(next_depth > last_depth)
    increases += 1
  end

  first_depthlist = depthlist.shift
  puts("-- #{first_depthlist} -> #{next_depth}")
  #if(next_depth > depthlist.shift)
  if(next_depth > first_depthlist)
    average_increases += 1;
  end
  last_depth = next_depth;
  depthlist.push(next_depth);
end

puts("Increases: #{increases}")
puts("Average increases: #{average_increases}")

