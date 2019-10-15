#include <Sparki.h>  // include the sparki library
 
void setup()
{
  Serial1.begin(9600);
}
 
void loop()
{
  Serial1.println("Hello World");
  delay(1000);
}

