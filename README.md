# TLAWaveformParser

This project has the Python required to open the Tektronix TLA listing files for the SPI EEPROM and turning it into a byte stream

Expected format from TLA for SPI memory interface
```
[Vectors]
CS#[],SI/IO0[],SO/IO1[],WP#/IO2[],HOLD#/IO3[]
0  ,0     ,0     ,0      ,1
...
```
