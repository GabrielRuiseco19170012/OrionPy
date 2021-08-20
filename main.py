from ApiRequest import ApiConsumption
from NewPerson import Person
import websocket
DOORBELL_PIN = 4
class Doorbell:
    def __init__(self, doorbell_button_pin):
        self._doorbell_button_pin = doorbell_button_pin

    def run(self):
        try:
            print("Starting Doorbell...")
            self._setup_gpio()
            print("Waiting for doorbell rings...")
            self._wait_forever()

        except KeyboardInterrupt:
            print("Safely shutting down...")

        finally:
            self._cleanup()

    def _wait_forever(self):
        while True:
            time.sleep(0.1)

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._doorbell_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._doorbell_button_pin, GPIO.RISING, callback=ring_doorbell, bouncetime=2000)

    def _cleanup(self):
        GPIO.cleanup(self._doorbell_button_pin)


GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)


def openDoor():
    GPIO.output(26, True)
    time.sleep(15)
    closeDoor()


def closeDoor():
    GPIO.output(26, False)


def on_message(ws, message):
    print(message)
    data = json.loads(message)
    event = data['d']['accion']
    if event == 'opening':
        openDoor()
    elif event == 'closing':
        closeDoor()


if __name__ == '__main__':
    r = ApiConsumption.login()
    doorbell = Doorbell(DOORBELL_PIN)
    doorbell.run()
    websocket.enableTrace(True)
    uri = "ws://chat-api-for-python-v0.herokuapp.com/adonis-ws"
    ws = websocket.WebSocketApp(uri,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                )
    ws.run_forever()
