
#include <klee/klee.h>

int f(int i1, int i2)
{
    int i = 0;
    int count = 0;
    while(i <= 5)
    {
        if (i1 <= 10) count++;
        if ((count >= 4) && (i2 >=90)) return 1;
        i++;
    }
    return 0;
}


int main() {
  int i1, i2;
  klee_make_symbolic(&i1, sizeof(i1), "i1");
  klee_make_symbolic(&i2, sizeof(i2), "i2");
  klee_assume((i1 <= 100)&(i1 >= 0));
  klee_assume((i2 <= 100)&(i2 >= 0));
  f(i1, i2);

} 
