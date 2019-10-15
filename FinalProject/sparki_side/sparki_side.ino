#include <Sparki.h> // include the sparki library


char str[110];
int len  = 0;
void setup()
{
Serial1.begin(9600);
}

void sendMessage(String str){
  Serial1.print(str);
  Serial1.print('#');
}

void recvMessage(char* str){
  while (Serial1.available())
  {
    int inByte = Serial1.read();
    
    if (inByte == '#'||len==100){
      str[len] = '\0';
      sparki.clearLCD(); 
      sparki.print(str);
      sparki.updateLCD();
      len = 0;// put the drawings on the screen
    }else{
      str[len++] = char(inByte);
    }
  }
}

void loop()
{
  char op[20] = {};
  while (op[0] != 's'){
    op[0] = 0;
    recvMessage(op);
    sparki.clearLCD(); 
      sparki.print(op);
    sparki.updateLCD();
    switch(op[0]){
      case 'f':sparki.moveForward(5);break;
      case 'r':sparki.moveRight(90);break; 
      case 'l':sparki.moveLeft(90);break; 
      case 'b':sparki.moveLeft(180);break;
      case 'o':
        sparki.gripperOpen(); 
        delay(4000);
        sparki.gripperStop(); 
        break;
      case 'c': sparki.gripperClose();
        delay(4000); 
        sparki.gripperStop();
        break;
    }
    sparki.moveStop(); 
    if (op[0] != 0)
      sendMessage("ok");
  }
}
