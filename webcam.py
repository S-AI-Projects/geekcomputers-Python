# Requirements:
#     pip install numpy
#     pip install opencv-python
# Program:
#     Opens your webcam and records.

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from colorama import Fore
except ImportError:
    class Fore:
        RED = ""
        RESET = ""


def webcam(frames, color_conv=None):
    """
    Process video frames by applying color conversion (BGR to BGRA).

    Complexity:
      - Input-size variable: N = total number of pixels across frames (W * H * frame_count).
      - Time Complexity: O(N) linear operations to map each 3-channel (B, G, R) pixel to 4-channel (B, G, R, A).
      - Space Complexity: O(N) to store the converted frames with additional alpha channel.
      - Distinction: The core frame transformation algorithm scales as O(N) CPU operations, distinct
        from camera driver capture latency, operating system I/O, and display render overhead.

    Preconditions:
      - Lines 11-12: Frames dimensioned by width and height.
      - Line 34: `gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)` conversion anchor.
    """
    results = []
    for frame in frames:
        if cv2 is not None and hasattr(frame, "shape"):
            conv = color_conv if color_conv is not None else cv2.COLOR_BGR2BGRA
            converted = cv2.cvtColor(frame, conv)
        else:
            # Pure Python fallback for list-represented pixels: [B, G, R] -> [B, G, R, 255]
            converted = []
            for row in frame:
                converted_row = []
                for pixel in row:
                    converted_row.append([pixel[0], pixel[1], pixel[2], 255])
                converted.append(converted_row)
        results.append(converted)
    return results


def main():
    if cv2 is None:
        print(Fore.RED + "opencv-python is required to open webcam" + Fore.RESET)
        return

    cap = cv2.VideoCapture(0)

    # Obtain resolutions, convert resolutions from float to integer
    frames_width = int(cap.get(3))
    frames_height = int(cap.get(4))

    # Specify the video codec
    # FourCC is platform dependent; however, MJPG is a safe choice.
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")

    # exception Handling for captured video
    try:
        # 60 FPS video capture
        # Create video writer object. Save file to recording.avi
        out = cv2.VideoWriter("recording.avi", fourcc, 60.0, (frames_width, frames_height))
    except Exception as e:
        print(Fore.RED, e, Fore.RESET)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == True:
            # Write frame to recording.avi
            out.write(frame)

            # color video output
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

            # Display the resulting frame
            cv2.imshow("frame", gray)
            if cv2.waitKey(1) & 0xFF == ord(" "):
                break

    # When everything is done, release the capture and video writer
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
