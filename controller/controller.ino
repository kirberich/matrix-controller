#include <Adafruit_GFX.h>
#include <RGBmatrixPanel.h> // Hardware-specific library
#include "controller.h"

byte x = 0;
byte y = 0;

byte got_header_bytes = 0;
boolean got_first_color_byte = false;
boolean in_frame = false;
uint16_t color;
byte val;
byte colorspace = 0;

void setup() {
  Serial.begin(200000);
  matrix.begin();
  digitalWrite(13, HIGH);
}


void draw_pixel() {
  if (y <= 31) {
    matrix.drawPixel(x, y, color);
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
    Serial.println("x");
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
  if(Serial.available()) {
    val = Serial.read();
  } else {
    return;
  }

  if (!in_frame && check_headers()) {
    return;
  }
  
  if (in_frame) {
    // 16 bit colors
    if (got_first_color_byte) {
      color |= val;
      draw_pixel();
      got_first_color_byte = false;
    } else {
      color = val;
      color = color << 8;
      got_first_color_byte = true;
    }
  }
}
