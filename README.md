# Setup v2lsrc module

Taken from https://www.dev47apps.com/droidcam/linux/

- Close any programs using the droidcam webcam. Unload the driver:
```bash
sudo rmmod v4l2loopback_dc
```

2. Re-load it with new options (WIDTH and HEIGHT are numbers). :

```bash
sudo insmod /lib/modules/`uname -r`/kernel/drivers/media/video/v4l2loopback-dc.ko width=WIDTH height=HEIGHT
```

Standard sizes (Width x Height): 640×480, 960×720, 1280×720 (720p), 1920×1080 (1080p).
