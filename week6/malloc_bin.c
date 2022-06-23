// 
// step2022 -week6-
// >>>> malloc challenge! <<<<
// 2. freelist binを実装する。
//

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);


typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;


typedef struct my_heap_t {
  my_metadata_t *free_head;
  my_metadata_t dummy;
  size_t maxsize; //このリストに入れる空き領域の最大のsize
} my_heap_t;


my_heap_t my_heap[4];
int num_list = 4;
static int num_challege = 0;


void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  int i = 0;
  while(my_heap[i].maxsize < metadata->size) i++; //metadataのサイズを見て、どの空き領域リストに入れるか決める
  
  //元々のリストの先頭要素を自分の次にして、自分をリストの先頭にする
  metadata->next = my_heap[i].free_head;
  my_heap[i].free_head = metadata;
}


void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {

  //removeする領域がリストの
  if (prev) { //先頭じゃなかったら、ただ前の要素のポインタnextを変更する
    prev->next = metadata->next;
  } else { //先頭だったら、リストの先頭要素を指すポインタfree_headを更新する
    int i = 0;
    while(my_heap[i].maxsize < metadata->size) i++; //metadataのサイズを見て、どの空き領域リストにあったか探す
    my_heap[i].free_head = metadata->next;
  }
  metadata->next = NULL;
}


// This is called at the beginning of each challenge.
void my_initialize() {

  int sizes[4] = {0, 1024, 2048, 4096};

  num_challege ++;
  for(int i=0; i<num_list; i++){
    my_heap[i].free_head = &my_heap[i].dummy;
    my_heap[i].dummy.size = 0;
    my_heap[i].dummy.next = NULL;
    my_heap[i].maxsize = sizes[i];
  }

  //0番目の空き領域リストは、小さすぎてmallocできない領域たちを入れる
  //それぞれのchallengeで与えられるsizeの最小値-1
  switch (num_challege)
  {
    case 1:
      my_heap[0].maxsize = 127;
      break;

    case 2:
      my_heap[0].maxsize = 15;
      break;
    
    case 3:
      my_heap[0].maxsize = 15;
      break;
    
    case 4:
      my_heap[0].maxsize = 255;
      break;
    
    case 5:
      my_heap[0].maxsize = 255;
      break;
  
    default:
      printf("ERROR: num_challenge\n");
      exit(1);
  }
}


// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <= 4000
void *my_malloc(size_t size) {
  
  //最もちょうどいいsizeの空き容量がありそうなリストから探し始める
  int i = 0;
  while(my_heap[i].maxsize < size) i++;

  my_metadata_t *metadata;
  my_metadata_t *prev;
  my_metadata_t *best_prev;
  my_metadata_t *best_metadata;
  size_t best_metadata_size;

  while(i < num_list){
    //変数の初期化
    metadata = my_heap[i].free_head; //i番目の空き容量リストの先頭をセット
    prev = NULL;
    best_prev = NULL;
    best_metadata = NULL;
    best_metadata_size = SIZE_MAX;

    while (metadata) { //i番目の空き領域リストを最後まで見る

      //best空き容量よりも小さい、かつ、mallocしたいsizeよりも大きかったら、bestを更新
      if(best_metadata_size > metadata->size && metadata->size >= size){
        best_prev = prev;
        best_metadata = metadata;
        best_metadata_size = metadata->size;
      }
      prev = metadata;
      metadata = metadata->next;
    }

    //prev, metadataをbestに書き換える
    prev = best_prev;
    metadata = best_metadata;

    //mallocする領域が決まったら抜ける
    if (metadata) break;

    //metadataが空だったら、i番目の空き領域リストには適切な領域がなかったということなので、
    //次に大きい空き領域リストを見ていく
    i++;
  }

  //全ての空き領域リストを見ても、sizeをmallocできる領域がなかったら、OSにメモリをもらって、もう一度mallocを行う
  if (!metadata) {
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;

    my_add_to_free_list(metadata);
    return my_malloc(size);
  }
  
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;

  //mallocする領域(metadata)が何番目の空き容量リストにあるかわからなくなってしまわないよう、
  //空き領域リストからremoveした後、mallocする領域のsizeを更新する
  my_remove_from_free_list(metadata, prev);
  metadata->size = size;

  if (remaining_size > sizeof(my_metadata_t)) {
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata);
  }
  return ptr;
}

// This is called every time an object is freed.
void my_free(void *ptr) {
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
}

void test() {
  assert(1 == 1);
}
