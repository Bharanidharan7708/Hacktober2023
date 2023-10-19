# Insertion sort in Python
def insertionSort(array):
  # Loop from the second element to the end of the array
  for i in range(1, len(array)):
    # Store the current element as key
    key = array[i]
    # Compare key with each element on the left of it until an element smaller than it is found
    j = i - 1
    while j >= 0 and key < array[j]:
      # Shift the element to the right by one position
      array[j + 1] = array[j]
      j = j - 1
    # Insert key at the correct position
    array[j + 1] = key

# Test the function with an example array
data = [9, 5, 1, 4, 3]
insertionSort(data)
print('Sorted Array in Ascending Order:')
print(data)
