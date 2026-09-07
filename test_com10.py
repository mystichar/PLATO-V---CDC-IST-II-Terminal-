"""Test connection to CDC IST-II terminal on COM10 per documentation."""
import time
import serial

PORT = "COM10"
PLATO_BAUD_RATES = [1200, 120, 150, 75]


def listen(ser: serial.Serial, seconds: float) -> list[tuple[float, bytes]]:
    chunks: list[tuple[float, bytes]] = []
    start = time.time()
    while time.time() - start < seconds:
        waiting = ser.in_waiting
        if waiting:
            data = ser.read(waiting)
            chunks.append((time.time() - start, data))
        else:
            time.sleep(0.05)
    return chunks


def format_data(data: bytes) -> str:
    hex_str = " ".join(f"{b:02X}" for b in data)
    ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in data)
    return f"{hex_str}  |{ascii_str}|"


def main() -> None:
    print("=" * 60)
    print("CDC IST-II PLATO Terminal - COM10 Connection Test")
    print("=" * 60)

    try:
        ser = serial.Serial(
            port=PORT,
            baudrate=1200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.5,
        )
    except serial.SerialException as exc:
        print(f"FAILED to open {PORT}: {exc}")
        return

    print(f"Opened {PORT} successfully")
    ser.dtr = True
    ser.rts = True
    time.sleep(0.2)

    print("\nModem control lines:")
    print(f"  DSR={ser.dsr}  CD={ser.cd}  CTS={ser.cts}  RI={ser.ri}")

    print("\nBaud rate scan (3s each, PLATO documented rates):")
    for baud in PLATO_BAUD_RATES:
        ser.baudrate = baud
        time.sleep(0.1)
        chunks = listen(ser, 3.0)
        if chunks:
            total = sum(len(c[1]) for c in chunks)
            print(f"  {baud:4d} bps: {total} bytes received")
            for elapsed, data in chunks:
                print(f"    [{elapsed:5.1f}s] {format_data(data)}")
        else:
            print(f"  {baud:4d} bps: no data")

    print("\nExtended listen at 1200 bps for 20 seconds...")
    ser.baudrate = 1200
    chunks = listen(ser, 20.0)
    if chunks:
        total = sum(len(c[1]) for c in chunks)
        print(f"  Received {total} bytes in {len(chunks)} chunk(s)")
        for elapsed, data in chunks:
            print(f"    [{elapsed:5.1f}s] {format_data(data)}")
    else:
        print("  No data received")

    print("\nSending marking idle (0xFF bytes) to simulate host NO-OP stream...")
    ser.write(bytes([0xFF] * 21))
    time.sleep(0.5)
    if ser.in_waiting:
        data = ser.read(ser.in_waiting)
        print(f"  Response: {format_data(data)}")
    else:
        print("  No response to idle bytes")

    ser.close()
    print("\nTest complete.")


if __name__ == "__main__":
    main()
