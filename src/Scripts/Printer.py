import sys
import time
from enum import Enum

class Printer:

    def print_hand_info(self, hand_data)->str:
        direction = hand_data.hand_direction
        str_hand_direction = str(direction.name if isinstance(direction, Enum) else direction)
        str_hand_factor = str(hand_data.hand_factor)
        str_hand_threshold = str(hand_data.hand_threshold)

        return (f"Hand Direction:{str_hand_direction}\033[K\n"
        f"Hand Factor:{str_hand_factor}\033[K\n"
        f"Hand Threshold:{str_hand_threshold}\033[K\n")

    def print_raw_positions(self, hand_data) -> str:
        str_raw_positions = str(hand_data.raw_positions)
        return f"Raw Positions:{str_raw_positions}\033[K\n"

    def print_pairwise_distances(self, hand_data) -> str:
        str_pairwise_distances = str(hand_data.pairwise_distances)
        return f"Pairwise Distances:{str_pairwise_distances}\033[K\n"

    def print_pairwise_angles(self, hand_data) -> str:
        str_pairwise_angles = str(hand_data.pairwise_angles)
        return f"Pairwise Angles:{str_pairwise_angles}\033[K\n"

    def print_all_data(self, hand_data):
        output = "\033[H=== TERMINAL OUTPUT ===\033[K\n"

        output += self.print_hand_info(hand_data)
        output += self.print_raw_positions(hand_data)
        output += self.print_pairwise_distances(hand_data)
        output += self.print_pairwise_angles(hand_data)

        output += "\033[J"

        sys.stdout.write(output)
        sys.stdout.flush()


'''
========================
MOCK DATA (test of code)
========================
'''

if __name__ == "__main__":
    class HandDirection(Enum):
        LEFT = "Left"
        RIGHT = "Right"
        UNKNOWN = "Unknown"

    class HandsData:
        def __init__(self, raw_positions, pairwise_distances, pairwise_angles, hand_direction, hand_factor, hand_threshold):
            self.raw_positions = raw_positions
            self.pairwise_distances = pairwise_distances
            self.pairwise_angles = pairwise_angles
            self.hand_direction = hand_direction
            self.hand_factor = hand_factor
            self.hand_threshold = hand_threshold

    printer = Printer()
    counter = 0

    while True:
        mock_data = HandsData(
            raw_positions={"x": counter, "y": counter^2},
            pairwise_distances={"thumb_index": 5.0 + (counter%5)},
            pairwise_angles={"thumb_joint": 45.0 + (counter%10)},
            hand_direction=HandDirection.RIGHT,
            hand_factor=1.25,
            hand_threshold=0.85
        )

        printer.print_all_data(mock_data)
        counter += 1

        time.sleep(1/30)