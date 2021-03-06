#include <stdio.h>
#include <stdlib.h>
#include "avlrot.h"

/* inputs: 100 200 150 work to balance via majorRminorL */

int main(void) {
   avlNode *root = NULL;
   int add = 0;
   while (scanf("%d", &add) != EOF) {
      add_avl(&root, add);
   }
   printf("\n   POST ORDER:\n\n");
   printf("Balance is: %d\n", isAVL(&root));
   printTreeInOrder(root);
   printf("\n   NEW ORDER:\n\n");
   dblrotate(&(root), 1); 
   printf("Balance is: %d\n", isAVL(&root));
   printTreeInOrder(root);
   printf("\nEND MAIN\n");
   return 0;
}
