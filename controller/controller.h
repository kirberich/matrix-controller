#define CLK 8  // MUST be on PORTB! (Use pin 11 on Mega)
#define OE  9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2
#define D   A3
RGBmatrixPanel matrix(A, B, C, D, CLK, LAT, OE, false);

#define COLOR16 0
#define COLOR1  1

// Address for this panel
// First three bytes are always the same
// Fourth one identifies the panel
byte address[] = {
  B10101010,
  B01010101,
  B11001100,
  B00010001 // Panel id
};
