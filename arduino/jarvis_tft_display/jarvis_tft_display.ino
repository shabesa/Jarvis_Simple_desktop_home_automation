#include <MCUFRIEND_kbv.h>
MCUFRIEND_kbv tft;       // hard-wired for UNO shields anyway.
#include <TouchScreen.h>

const int YM=6,YP=A2,XM=A1,XP=7;
const int TS_LEFT=907,TS_RT=136,TS_TOP=942,TS_BOT=139;

char data;

TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);
TSPoint tp;

#define MINPRESSURE 200
#define MAXPRESSURE 1000

#define TS_MINX 940
#define TS_MINY 160
#define TS_MAXX 160
#define TS_MAXY 970

int16_t BOXSIZE;
int16_t PENRADIUS = 3;
uint16_t ID, oldcolor, currentcolor;

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
