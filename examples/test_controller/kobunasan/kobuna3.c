#include <klee/klee.h>

#define RUN 4

int f(int i1, int i2, int* p_count)
{
    if (i1 <= 10) (*p_count)++;
    if (((*p_count) >= 4) && (i2 >= 90)) return 1;
    return 0;
}


int main() {
  int i1, i2;
  int i = 0;
  int count;
  int ret;
  klee_make_symbolic(&i1, sizeof(i1), "i1");
  klee_make_symbolic(&i2, sizeof(i2), "i2");
  klee_make_symbolic(&count, sizeof(count), "count");

#if RUN == 1
  //count = 0;
  klee_assume(((i1 <= 100)&(i1 >= 0))&((i2 <= 100)&(i2 >= 0)));
  klee_assume((count >= 0)&(count <= 0));
#elif RUN == 2
  //count = 1;
  klee_assume(((i1 <= 100)&(i1 >= 0))&((i2 <= 100)&(i2 >= 0)));
  klee_assume((count >= 0)&(count <= 1));

#elif RUN == 3
  //count = 2;
  klee_assume(((i1 <= 100)&(i1 >= 0))&((i2 <= 100)&(i2 >= 0)));
  klee_assume((count >= 0)&(count <= 2));

#elif RUN == 4
  //count = 2;
  klee_assume(((i1 <= 100)&(i1 >= 0))&((i2 <= 100)&(i2 >= 0))&((count >= 0)&(count <= 3)));
#endif
  //klee_assume(((i1 == 11)&(i2 == 0)&(count == 0))|((i1 == 0)&(i2 == 0)&(count == 1)));

  ret = f(i1, i2, &count);
  klee_assert(ret == 0);

return 0;
} 
