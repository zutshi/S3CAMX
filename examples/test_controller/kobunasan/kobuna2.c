

#include <klee/klee.h>

int f(int i1, int i2, int* p_count)
{
    if (i1 <= 10) (*p_count)++;
    if (((*p_count) >= 4) && (i2 >= 90)) return 1;
    return 0;
}


int main() {
  int i1[5], i2[5];
  int i = 0;
  int count = 0;
  int ret;
  //int ret2;
  klee_make_symbolic(&i1, sizeof(i1), "i1");
  klee_make_symbolic(&i2, sizeof(i2), "i2");

  //klee_make_symbolic(&ret2, sizeof(ret2), "ret2");

  klee_assume((i1[0] <= 100)&(i1[0] >= 0));
  klee_assume((i1[1] <= 100)&(i1[1] >= 0));
  klee_assume((i1[2] <= 100)&(i1[2] >= 0));
  klee_assume((i1[3] <= 100)&(i1[3] >= 0));
  klee_assume((i1[4] <= 100)&(i1[4] >= 0));

  klee_assume((i2[0] <= 100)&(i2[0] >= 0));
  klee_assume((i2[1] <= 100)&(i2[1] >= 0));
  klee_assume((i2[2] <= 100)&(i2[2] >= 0));
  klee_assume((i2[3] <= 100)&(i2[3] >= 0));
  klee_assume((i2[4] <= 100)&(i2[4] >= 0));

/*
  while(i < 5)
  {
      ret = f(i1[i], i2[i], &count);
      klee_assert(ret == 0);
      i++;
  }
*/ 

  ret = f(i1[0], i2[0], &count);
  klee_assert(ret == 0);

  ret = f(i1[1], i2[1], &count);
  klee_assert(ret == 0);

  ret = f(i1[2], i2[2], &count);
  klee_assert(ret == 0);

  ret = f(i1[3], i2[3], &count);
  klee_assert(ret == 0);

  ret = f(i1[4], i2[4], &count);
  klee_assert(ret == 0);
return 0;
} 
