'''
Renames all four-digit .out files in the current directory from ascending to descending order
coding:UTF-8
env:base
'''

import os
import re

def reverse_rename_out_files():
  """
  Renames all four-digit .out files in the current directory from ascending to descending order.
  Example: 0001.out, 0002.out, 0003.out become 0003.out, 0002.out, 0001.out
  """
  # Get all files in current directory
  files = os.listdir('.')
  
  # Filter for four-digit .out files using regex pattern
  pattern = re.compile(r'^\d{4}\.out$')
  out_files = [f for f in files if pattern.match(f)]
  
  # Check if we found any matching files
  if not out_files:
    print("No four-digit .out files found in current directory.")
    return
  
  # Sort files in ascending order
  out_files.sort()
  
  # Create mapping: original file -> new file name
  file_count = len(out_files)
  rename_map = {}
  
  # Create reverse mapping (first becomes last, etc.)
  for i in range(file_count):
    original = out_files[i]
    
    # Calculate new position (reverse order)
    reverse_index = file_count - 1 - i
    
    # Get the original number from the reverse position file
    original_number = out_files[reverse_index][:4]
    
    # Create new filename with original number
    new_name = f"{original_number}.out"
    rename_map[original] = new_name
  
  # Display what will be renamed
  print(f"Found {file_count} four-digit .out files:")
  for original, new_name in rename_map.items():
    print(f"  {original} -> {new_name}")
  
  # Ask for confirmation
  response = input("\nProceed with renaming? (y/n): ").strip().lower()
  if response != 'y':
    print("Renaming cancelled.")
    return
  
  # Perform the renaming
  renamed_count = 0
  errors = []
  
  for original, new_name in rename_map.items():
    try:
      # Check if source file exists
      if not os.path.exists(original):
        errors.append(f"Source file not found: {original}")
        continue
      
      # Check if target file already exists (should not happen with this algorithm)
      if os.path.exists('temp'+new_name):
        errors.append(f"Target file already exists: temp{new_name}")
        continue
      
      # Rename the file
      os.rename(original, 'temp'+new_name)
      renamed_count += 1
      print(f"Renamed: {original} -> temp{new_name}")
      
    except Exception as e:
      errors.append(f"Error renaming {original} to {new_name}: {str(e)}")
  
  # Display results
  print(f"\nRenaming complete:")
  print(f"  Successfully renamed: {renamed_count} files")
  if errors:
    print(f"  Errors: {len(errors)}")
    for error in errors:
      print(f"    {error}")
  for original, new_name in rename_map.items():
    os.rename('temp'+new_name, new_name)
if __name__ == "__main__":
  reverse_rename_out_files()
  input("\nPress Enter to exit...")