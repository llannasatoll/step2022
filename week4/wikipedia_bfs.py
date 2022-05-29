"""
step2022 -week4-
”Google”から”渋谷”をたどる経路を、DFSで探す
"""

import collections
import time 

id_to_title = {}
id_to_nextIDs = {}
id_to_parentID = {} #ID => たどってきた直前のnodeのID のmapping

#Breadth-First Search
def bfs(startID, targetID):
  """
  Find if there is a path between two points using DFS.
  Args:
    startID: the start title ID
    targetID: the goal title ID

  Returns: True if it exists, false otherwise.
  """
  queue = collections.deque() #キュー（探索対象node）の初期化
  queue.append(startID) #キューの先頭にstartのnodeを入れる
  id_to_parentID[startID] = -1 #startは親nodeがいないので、-1とする
  
  while queue: #キューが空になるまで
    first = queue.popleft() #先頭のnodeを探索nodeとする
    if first == targetID:
      return True

    if first in id_to_nextIDs: #アクセスできるnodeがあったら
      for nextID in id_to_nextIDs[first]: #そのnodeを全て見る
        if nextID not in id_to_parentID: #親nodeがなかったら = 未探索だったら
          id_to_parentID[nextID] = first #親nodeを自分に設定し、
          queue.append(nextID) #キューの最後に追加

  return False

#たどってきたnodeを全て記録して探索していくBFS
#距離が遠くなると実行時間がかなり伸びてしまうので、今回は上の方法を採用しました。
"""
def bfs(startID, targetID):
  ""
  Return the BSF path between two points.
  Args:
    startID: the start title ID
    targetID: the goal title ID

  Returns: the path if it exists, none otherwise
  ""
  queue = collections.deque()
  queue.append([startID])

  while queue:
    path = queue.popleft()
    node = path[-1]
    if node == targetID:
      return path

    if node in id_to_nextIDs:
      for nextID in id_to_nextIDs[node]:
        new_path = path.copy()
        new_path.append(nextID)
        queue.append(new_path)

  return None
"""

def search_route(targetID):
  """
  Retrace the parent node to get the path.

  Args:
    targetID: the ID of the current node

  Returns: the path(list) between two points

  Raises: error if the goal isn't in the graph
  """
  if id_to_parentID[targetID] == -1: #-1だったらstart node
    return [targetID]

  try:
    ans = search_route(id_to_parentID[targetID])
  except KeyError:
    print("ERROR : Can't find the (ID)%s\'s parent node." %targetID)
    exit(1)
  ans.append(targetID)
  return ans


def main():
  #Set your path.
  pages_data = "data/pages.txt"
  links_data = "data/links.txt"

  print("Now Loading...")

  #Create a dictionary that maps ID to page title.
  with open(pages_data) as f:
    for data in f.read().splitlines():
      page = data.split("\t")
      id_to_title[page[0]] = page[1]

  #Create a dictionary that maps ID to the list of accessible nodes.
  with open(links_data) as f:
    for data in f.read().splitlines():
      link = data.split("\t")
      if link[0] in id_to_nextIDs:
        id_to_nextIDs[link[0]].add(link[1])
      else:
        id_to_nextIDs[link[0]] = {link[1]}

  
  # Input start word.
  while True:
    start = input("START : ")
    for k, v in id_to_title.items():
      if start == v:
        startID = k
        break
    else:
      print("The page \"%s\" does not exists." %start)
      continue
    break

  #Input goal word.
  while True:
    goal = input("GOAL : ")
    for k, v in id_to_title.items():
      if goal == v:
        targetID = k
        break
    else:
      print("The page \"%s\" does not exists." %goal)
      continue
    break

  print("Searching path from \"%s\" to \"%s\"" %(start, goal))

  if bfs(startID, targetID):
    ans = search_route(targetID)
    print(" -> ".join([id_to_title[id_] for id_ in ans]))
  else:
    print("From \"%s\" to \"%s\" can not be reached." %(start, goal))


if __name__ == "__main__":
    main()