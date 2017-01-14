#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <time.h>
#include <errno.h>

int main(void) {

  int fd = open("/dev/i2c-4", O_RDWR);
  if(fd < 0) {
    fprintf(stderr,"error: no device found\n");
    exit(-1);
  }

  int status = ioctl(fd, I2C_SLAVE, 0x48);
  if(status < 0) {
    fprintf(stderr,"error\n");
    exit(-1);
  }

//  int logfd = open("/home/thibault/Temperature/temp.csv", O_APPEND|O_WRONLY);
//  if(logfd < 0) {
//    fprintf(stderr,"error: cannot open log file\n");
//    exit(-1);
//  }

  uint8_t raw[2];
  int n = read(fd, &raw, 2);
  if(n == 2) {
    // change endianness
    uint16_t rawv = raw[1] | raw[0] << 8;
    // convert to temperature
    // RTFM: http://www.ti.com.cn/cn/lit/ds/symlink/tmp102.pdf
    float temp = ((int16_t)rawv>>4)*0.0625;

    // format current time
    time_t now;
    time(&now);
    char sdate[256];
    strftime(sdate, sizeof(sdate), "\"%Y-%m-%d %H:%M:%S\"", localtime(&now));

    // format csv line
    char smsg[256];
    int wn = snprintf(smsg, sizeof(smsg), "%s;%1.1f\n", sdate, temp);
    if(wn <= 0) {
      fprintf(stderr,"error\n");
      exit(-1);
    }

//    int on = write(logfd, smsg, wn);
    fprintf(stdout,"%1.1f", temp);
//    if(on <= 0) {
//      fprintf(stderr,"error\n");
//      exit(-1);
//    }
  }

  return 0;
}
