RGBmatrixPanelDue matrix(MATRIX_32_32, 1, 1, 3);

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
