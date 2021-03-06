"""
step2022 -week2-
4. Design a cache that achieves the following operations with mostly O(1)
  ・When a pair of <URL, Web page> is given, find if the given pair is contained in the cache or not
  ・If the pair is not found, insert the pair into the cache after evicting the least recently accessed pair
"""

import sys
import time

# Cache is a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library (e.g., collections.OrderedDict).
#       Implement the data structure yourself.

class Cache:
  # Initializes the cache.
  # |n(int)|: The size of the cache.
  def __init__(self, n):
    self.n = n
    self.list = DoublyLinkedList()
    self.url_to_contents = {}

  # Access a page and update the cache so that it stores the most
  # recently accessed N pages. This needs to be done with mostly O(1).
  # |url|: The accessed URL
  # |contents|: The contents of the URL
  def access_page(self, url, contents):
    if url in self.url_to_contents:
      node = self.url_to_contents[url]
      self.list.delete(node)
      self.list.insert(node)
    else: 
      if len(self.url_to_contents) >= self.n:
        tail_node = self.list.tail.prev
        self.list.delete(tail_node)
        del self.url_to_contents[tail_node.url]

      new_node = Node(url, contents)
      self.list.insert(new_node)
      self.url_to_contents[url] = new_node

  # Return the URLs stored in the cache. The URLs are ordered
  # in the order in which the URLs are mostly recently accessed.
  def get_pages(self):
    res = []
    node = self.list.head.next
    while node.url is not None:
      res.append(node.url)
      node = node.next
    return res

class Node:
  # Initializes the node of Doubly Linked List.
  # Each node has the URL and the contents.
  def __init__(self, url, contents):
    self.url = url
    self.contents = contents
    self.next = None
    self.prev = None

class DoublyLinkedList:
  # Initializes the Doubly Linked List.
  # head.next -> the beginning of the list
  # tail.prev -> the end of the list
  def __init__(self):
    self.head = Node(None, None)
    self.tail = Node(None, None)
    self.head.next = self.tail
    
  # Insert a node that has the URL and the contents at the beginning of the list.
  # Return the node.
  def insert(self, newnode):
    newnode.next = self.head.next
    self.head.next.prev = newnode
    self.head.next = newnode
    newnode.prev = self.head 

  # Delete the node.
  # Return the URL that the node had.
  def delete(self, node):
    if node.next is None and node.prev is None:
      pass
    else:
      node.prev.next = node.next
      node.next.prev = node.prev

# Does your code pass all test cases? :)
def cache_test():
  # Set the size of the cache to 4.
  cache = Cache(4)
  # Initially, no page is cached.
  equal(cache.get_pages(), [])
  # Access "a.com".
  cache.access_page("a.com", "AAA")
  # "a.com" is cached.
  equal(cache.get_pages(), ["a.com"])
  # Access "b.com".
  cache.access_page("b.com", "BBB")
  # The cache is updated to:
  #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["b.com", "a.com"])
  # Access "c.com".
  cache.access_page("c.com", "CCC")
  # The cache is updated to:
  #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["c.com", "b.com", "a.com"])
  # Access "d.com".
  cache.access_page("d.com", "DDD")
  # The cache is updated to:
  #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
  # Access "d.com" again.
  cache.access_page("d.com", "DDD")
  # The cache is updated to:
  #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
  # Access "a.com" again.
  cache.access_page("a.com", "AAA")
  # The cache is updated to:
  #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
  equal(cache.get_pages(), ["a.com", "d.com", "c.com", "b.com"])
  cache.access_page("c.com", "CCC")
  equal(cache.get_pages(), ["c.com", "a.com", "d.com", "b.com"])
  cache.access_page("a.com", "AAA")
  equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
  cache.access_page("a.com", "AAA")
  equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
  # Access "e.com".
  cache.access_page("e.com", "EEE")
  # The cache is full, so we need to remove the least recently accessed page "b.com".
  # The cache is updated to:
  #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
  equal(cache.get_pages(), ["e.com", "a.com", "c.com", "d.com"])
  # Access "f.com".
  cache.access_page("f.com", "FFF")
  # The cache is full, so we need to remove the least recently accessed page "c.com".
  # The cache is updated to:
  #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
  equal(cache.get_pages(), ["f.com", "e.com", "a.com", "c.com"])
  # Access "e.com".
  cache.access_page("e.com", "EEE")
  # The cache is updated to:
  #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
  equal(cache.get_pages(), ["e.com", "f.com", "a.com", "c.com"])
  # Access "a.com".
  cache.access_page("a.com", "AAA")
  # The cache is updated to:
  #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
  equal(cache.get_pages(), ["a.com", "e.com", "f.com", "c.com"])
  print("OK!")

# A helper function to check if the contents of the two lists is the same.
def equal(list1, list2):
  #print("list1 : ", list1)
  #print("list2 : ", list2)
  assert(list1 == list2)

def cache_test2(n):
  cache = Cache(n)

  begin = time.time()
  for i in range(100000):
    cache.access_page(str(0)+".com", chr(0))
    cache.access_page(str(i)+".com", chr(i))
  end = time.time()

  print("time : ", end - begin)

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("usage: %s [cache size]" % sys.argv[0])
    exit(1)
    
  cache_test()
  cache_test2(int(sys.argv[1]))

