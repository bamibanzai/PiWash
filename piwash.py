#module written for the Raspberry Pi model 3 WiFi


try:
    import RPi.GPIO as RaspIO
    import time
    # import requests
    # import http.client, urllib #enables push notifications
    import logging #debug
except RuntimeError:
    print("Error loading RaspIO")

TIMEDELAY = 120 #Time to wait in seconds before declaring end of the cycle (2 mins)

#Define Raspberry Pi Input pins (in Number format)
BUTTON =
LED =
CURRENT =

def main():
    try:
        # Configure RaspIO pins
        RaspIO.setmode(RaspIO.BOARD)
        RaspIO.setup(CURRENT, RaspIO.IN)
        RaspIO.setup(LED, RaspIO.OUT)

        # "Pull-down" resistor must be added to input
        # push-button to avoid floating value at
        # RPi input when button not in closed circuit.
        RaspIO.setup(BUTTON, RaspIO.IN, pull_up_down=RaspIO.PUD_DOWN)

        # Start of sensing of upwards or downwards front on
        # pin connected to CURRENT detector.
        # "Bouncetime" argument ignores effect of bouncing caused by
        # sudden state changes.
        RaspIO.add_event_detect(CURRENT, RaspIO.BOTH, bouncetime=200)

        # Configure debugging journal file on RPi
        logging.basicConfig(filename='/home/pi/washer.log',
                            level=logging.INFO,
                            format='%(asctime)s %(levelname)s:%(message)s')
        logging.info("****************************")
        stop = False
        logging.info("Entering main loop")

        # Main loop, waits for push-button to be
        # pressed to indicate beginning of cycle, then
        # periodically checks CURRENT.
        while not stop:
            logging.info("Main loop iteration")
            RaspIO.output(LED, True)  # LED off
            RaspIO.wait_for_edge(BUTTON, RaspIO.RISING)  # wait for signal
            # from push-button
            logging.info(" Started")
            going = True
            RaspIO.output(LED, False)  # LED on

            # Secondary program circuit, checks every 3
            # minutes for CURRENTs during this time.
            # If no CURRENT for the last 3
            # minutes, cycle considered done.
            while going:
                logging.info("  Inner loop iteration")
                time.sleep(TIMEDELAY)
                logging.info("  Just slept %ds", TIMEDELAY)

                # Manual override to stop the current cycle;
                # keep push-button
                # pressed during check.
                if RaspIO.input(BUTTON):
                    stop = True
                    going = False

                # End of cycle if no CURRENT detected.
                if not RaspIO.event_detected(CURRENT):
                    logging.info("  Stopped vibrating")
                    pushdone()
                    going = False
            logging.debug(" End of iteration")
    except:
        logging.warning("Quit on exception")
    finally:
        logging.info("Cleaning up")
        RaspIO.remove_event_detect(CURRENT)
        RaspIO.cleanup()

# #Send push notification with Pushover API
# def pushdone():
#     conn = http.client.HTTPSConnection("api.pushover.net:443")
#     conn.request("POST", "/1/messages.json",
#                  urllib.parse.urlencode({
#                      "token": "<app key pushover.net>",
#                      "user": "<user key pushover.net>",
#                      "message": "Laundry is done",
#                  }), {"Content-type": "application/x-www-form-urlencoded"})
#     conn.getresponse()


if __name__ == '__main__': main()