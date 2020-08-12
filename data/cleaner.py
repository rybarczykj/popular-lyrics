# Open the file as read
f = open("songTable.csv", "r+")

# Create an array to hold write data
new_file = []
# Loop the file line by line
for line in f:
  if line.endswith(','):
    # Add
    new_file.append(line[:-1])
# Open the file as Write, loop the new array and write with a newline
with open("songTable.csv", "w+") as f:
  for i in new_file:
    f.write(i+"\n")