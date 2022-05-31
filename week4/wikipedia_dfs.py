"""
step2022 -week4-
”Google”から”渋谷”をたどる経路を、DFSで探す
"""
import sys
sys.setrecursionlimit(100000) #再起の上限を100000回に設定する

id_to_title = {}
id_to_nextIDs = {}
visited = set() #探索済みnodeを入れる集合

#Depth-First Search
def dfs(startID, targetID):
  """
  Return the DSF path between two points.
  Args:
    startID: the start title ID
    targetID: the goal title ID

  Returns: the path from goal to start if it exists, none otherwise
  """
  visited.add(startID) #探索済みにする

  if startID == targetID:
    return [targetID]

  if startID in id_to_nextIDs: #アクセスできるnodeがあったら
    for nextID in id_to_nextIDs[startID]: #そのnodeを全て見る
      if nextID not in visited: #まだ未探索だったら
        try:
            ans = dfs(nextID, targetID) #再起してさらに深く見ていく
        except RecursionError : #再起の上限に到達したら
            return None #それ以上の探索をやめる
        if ans is not None: #ansがNoneではなかったら = 探索先でgoalにたどり着いていたら
          ans.append(startID) #リストに自分を付け加えて返す
          return ans

  return None


def main():
  #Set your path.
  pages_data = "data/pages.txt"
  links_data = "data/links.txt"

  print("Now Loading...")

  #Create a dictionary that maps ID to title.
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

  #Input start word.
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
  ans = dfs(startID, targetID)
  if ans is None:
    print("From \"%s\" to \"%s\" can not be reached." %(start, goal))
  else:
    print(" -> ".join([id_to_title[id_] for id_ in ans[::-1]]))


if __name__ == "__main__":
    main()