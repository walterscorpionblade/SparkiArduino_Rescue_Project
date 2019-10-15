#include <Sparki.h> // include the sparki library


char str[110];
int len  = 0;
void setup()
{
Serial1.begin(9600);
}

void loop()
{
readComm();
}

void send_Message_with_BT(const char* str){
  Serial1.print(str);
  Serial1.print('#');
}

void readComm()
{
  while (Serial1.available())
  {
    int inByte = Serial1.read();
    
    if (inByte == '#'||len==100){
      str[len] = '\0';
      sparki.clearLCD(); 
      sparki.print(str);
      sparki.updateLCD();
      send_Message_with_BT("Nice to meet your!\n");
      delay(10000);
      len = 0;// put the drawings on the screen
    }else{
      str[len++] = char(inByte);
    }

  } 
  

}
