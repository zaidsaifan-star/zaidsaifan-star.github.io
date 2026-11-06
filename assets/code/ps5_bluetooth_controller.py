import pygame
import serial
import time

# ── Configuration ──────────────────────────────────────────────
BLUETOOTH_PORT = 'COM5'  # <--- CHANGE TO YOUR PORT
BAUD_RATE = 9600
UPDATE_RATE = 0.02
DEADZONE = 0.1

try:
    bt = serial.Serial(BLUETOOTH_PORT, BAUD_RATE, timeout=1)
    print("Bluetooth connected successfully!")
except Exception as e:
    print(f"Error connecting to Bluetooth: {e}")
    exit()

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected.")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()
print(f"Controller Connected: {controller.get_name()}")

# PS5 Controller Mappings
AXIS_STEER = 0
AXIS_L2 = 4
AXIS_R2 = 5
BTN_CROSS = 0  # The 'X' Button on PS5

last_command = ""
auto_mode = False
last_btn_state = False

print("\n--- PS5 Controls Active ---")
print("R2: Gas | L2: Brake/Reverse | L3: Steer")
print("Press 'X' to toggle Autopilot!")

try:
    while True:
        pygame.event.pump()

        # --- AUTOPILOT TOGGLE LOGIC ---
        btn_state = controller.get_button(BTN_CROSS)
        if btn_state and not last_btn_state:  # Button was just pushed down
            auto_mode = not auto_mode  # Toggle the state

            if auto_mode:
                bt.write(b"AUTO\n")
                print("\n[!] AUTOPILOT ENGAGED [!]\n")
            else:
                bt.write(b"MAN\n")
                print("\n[-] MANUAL CONTROL RESTORED [-]\n")

        last_btn_state = btn_state

        # --- MANUAL DRIVING LOGIC ---
        # We only calculate and send joystick data if Autopilot is OFF
        if not auto_mode:
            steer_axis = controller.get_axis(AXIS_STEER)
            l2_axis = controller.get_axis(AXIS_L2)
            r2_axis = controller.get_axis(AXIS_R2)

            if abs(steer_axis) < DEADZONE:
                steer_axis = 0.0

            brake = max(0.0, (l2_axis + 1.0) / 2.0)
            gas = max(0.0, (r2_axis + 1.0) / 2.0)

            throttle = gas - brake

            left_motor = throttle + steer_axis
            right_motor = throttle - steer_axis

            left_motor = max(-1.0, min(1.0, left_motor))
            right_motor = max(-1.0, min(1.0, right_motor))

            left_pwm = int(left_motor * 255)
            right_pwm = int(right_motor * 255)

            command = f"{left_pwm},{right_pwm}\n"

            if command != last_command:
                bt.write(command.encode('utf-8'))
                last_command = command
                # Only print the dashboard occasionally so it doesn't flood the terminal
                print(f"\rMANUAL >> L2: {brake:.2f} | R2: {gas:.2f} | Motor L: {left_pwm:4d} | Motor R: {right_pwm:4d}",
                      end="")

        time.sleep(UPDATE_RATE)

except KeyboardInterrupt:
    print("\nExiting. Stopping car...")
    bt.write(b"0,0\n")
    bt.close()
    pygame.quit()
