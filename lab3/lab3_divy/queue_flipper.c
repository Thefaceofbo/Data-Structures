#include <stdio.h>
#include <stdlib.h>

struct queue {
   int *store;
   int start;
   int end;
   int length;
   int flipped;  /* -1 = true, 1 = false */
};
typedef struct queue queue;

int init_queue(queue **in, int length);
int enqueue(queue *in, int new_data);
int dequeue(queue *in);
int peek(queue *in);

int init_queue(queue **in, int length) {
   if (in == NULL) {
      return -1;
   }
   *in = (queue *)malloc(sizeof(queue));
   (*in)->store = (int *)malloc(sizeof(int) * length);
   (*in)->start = 0;
   (*in)->end = -1;
   (*in)->length = length;
   (*in)->flipped = 1;
   return 0;
}

int enqueue(queue *in, int new_data) {
   if (in == NULL) {
      return -1;
   }
   else if (((in->end - in->start) * in->flipped) + 1 >= in->length) {
      return -1;
   }
   if (in->end + 1 == in->length) {
      in->end = 0;
      in->flipped *= -1;
   }
   else {
      in->end += 1;
   }
   (in->store)[in->end] = new_data;
   return 0;
}

int dequeue(queue *in) {
   int first = 0;
   if (in == NULL) {
      return -1;
   }
   else if ((in->end - in->start) * in->flipped == -1) {
      return -1;
   }
   first = (in->store)[in->start];
   if (in->start + 1 == in->length) {
      in->start = 0;
      in->flipped *= -1;
   }
   else {
      in->start += 1;
   }
   return first;
}

int peek(queue *in) {
   int i = 0;
   int amount = in->end - in->start + 1;
   if (in == NULL) {
      return -1;
   }
   if (in->flipped == -1) {
      amount = amount * in->flipped - in->length;
   }
   printf("[");
   for (i = in->start; i < in->start + amount; i++) {
      if (i >= in->length) {
         i = i - in->length;
      }
      printf("%d,", (in->store)[i]);
   }
   printf("]\n");
   return 0;
}

int main(void) {
   queue *q = NULL;
   init_queue(&q, 10);
   int i = 0;
   peek(q);
   for (i = 0; i < 10; i++) {
      enqueue(q, i);
      peek(q);
   }
   for (i = 0; i < 7; i++) {
      printf("Dequeued: %d\n", dequeue(q));
      peek(q);
   }
   
   return 0;
}