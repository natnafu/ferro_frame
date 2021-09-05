#ifndef TLC5940_H
#define TLC5940_H

void tlc_init();
void tlc_update();
void tlc_set(uint8_t channel, uint16_t value);
void tlc_set_all(uint16_t value);

#endif
