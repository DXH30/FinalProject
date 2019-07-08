#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>

// Mendefinisikan 1 Layer LSTM
// Fungsi aktivasi
float cell_state;
float hidden_state;
float input;

float sigmoid(float input) {
  return 1.0/(1.0+exp(input));
}

// Forget Gate
float forget_gate(float input, float cell_state) {
  return cell_state*sigmoid(input);
}

// Input Gate
float input_gate(float input, float cell_state) {
  return sigmoid(input)*tanh(input)+cell_state;
}

// Output Gate 
float output_gate(float input, float cell_state) {
  return sigmoid(input)*tanh(cell_state);
}

// Input adalah hidden state, setiap satu kali masuk
// Input xn akan dijumlahkan dengan hidden state hn
// Yang dihasilkan dari data hidden state sebelumnya

int update_weights() {
  cell_state = forget_gate(input, cell_state);
  cell_state = input_gate(input, cell_state);
  hidden_state = input_gate(input, cell_state);
  return 1;
}
// Data dari input state untuk update weights

int main(int argc, char **argv) {
  if (argc < 1) {
    printf("Usage : %s [options]\n", argv[0]);
    exit(0);
  } else {
    printf("Usage : %s is still in maintenance\n", argv[0]);
    exit(0);
  }
  return 0;
}
