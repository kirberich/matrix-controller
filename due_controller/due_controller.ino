#include "RGBmatrixPanelDue.h"
#include "controller.h"

byte x = 0;
byte y = 0;

byte got_header_bytes = 0;
boolean got_red = false;
boolean got_green = false;
boolean in_frame = false;
uint16_t color;
byte r, g, b;
byte val;
byte colorspace = 0;

void TC3_Handler()
{
  TC_GetStatus(TC1, 0);
  matrix.updateDisplay();
}

void setup() {
  SerialUSB.begin(200000);
  matrix.begin(8000);
}


void draw_pixel() {
  if (y <= 31) {
    matrix.drawPixel(x, y, matrix.Color888(r,g,b));
  }
  
  if (x == 31) {
    y++;
    x = 0;
  } else {
    x++;
  }
  
  if (y > 31) {
    // Mark state as out of frame when x and y reach 31, reset x and y
    in_frame = false;
    x = 0;
    y = 0;
    //SerialUSB.println("x");
  }
}

// Checks incoming values to see if they look like a header
// Returns true if byte is part of header and should be ignored
boolean check_headers() {
  if (got_header_bytes == 0 && val == address[0]){
    got_header_bytes = 1;
  } else if (got_header_bytes == 1 && val == address[1]) {
    got_header_bytes = 2;
  } else if (got_header_bytes == 2 && val == address[2]) {
    got_header_bytes = 3;
  } else if (got_header_bytes == 3 && val == address[3]) {
    got_header_bytes = 4;
  } else if (got_header_bytes == 4) {
    // Address matched, set color space and start 
    colorspace = val;
    got_header_bytes = 0;
    in_frame = true; // Set to true after header is over
    return true;
  } else {
    got_header_bytes = 0;
  }
  return false;
}

void loop() {
  if(SerialUSB.available()) {
    val = SerialUSB.read();
  } else {
    return;
  }

  if (!in_frame && check_headers()) {
    return;
  }
  
  if (in_frame) {
    // 16 bit colors
    if (!got_red) {
      r = val;
      got_red = true;
    } else if (!got_green) {
      g = val;
      got_green = true;
    } else {
      b = val;
      draw_pixel();
      got_red = false;
      got_green = false;
    }
  }
}
