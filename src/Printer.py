import sys
import hand as hand
import time
from enum import Enum

class Printer:

    def printHandInfo(self, Hand)->str:
        direction = hand.HandDirection
        str_handDirection = str(direction.name if isinstance(direction, Enum) else direction)
        str_handFactor = str(Hand.handFactor)
        str_handThreshold = str(Hand.handThreshold)
        str_rawPositions = str(Hand.rawPositions)

        return (f"Hand Direction:{str_handDirection}\033[K\n"
        f"Hand Factor:{str_handFactor}\033[K\n"
        f"Hand Threshold:{str_handThreshold}\033[K\n"
        f"Hand Positions:{str_rawPositions}\033[K\n")

    def print_rawPositions(self, Hand) -> str:
        str_rawPositions = str(Hand.rawPositions)
        return f"Raw Positions:{str_rawPositions}\033[K\n"

    def print_pairwise_distances(self, Hand) -> str:
        str_pairwise_distances = str(Hand.pairWiseDistances)
        return f"Pairwise Distances:{str_pairwise_distances}\033[K\n"

    def print_pairwise_angles(self, Hand) -> str:
        str_pairwise_angles = str(Hand.pairWiseAngles)
        return f"Pairwise Angles:{str_pairwise_angles}\033[K\n"

    def print_all_data(self, Hand):
        output = "\033[H=== TERMINAL OUTPUT ===\033[K\n"

        output += self.printHandInfo(Hand)
        output += self.print_rawPositions(Hand)
        output += self.print_pairwise_distances(Hand)
        output += self.print_pairwise_angles(Hand)
        output += self.print_rawPositions(Hand)


        output += "\033[J"

        sys.stdout.write(output)
        sys.stdout.flush()


'''
========================
MOCK DATA (test of code)
========================
'''

if __name__ == "__main__":
    printer = Printer()
    counter = 0

    while True:
        mockHand = hand.Hand()
        mockHand.handFactor = 0.0
        mockHand.handThreshold = 0.0
        mockHand.rawPositions = {"x":counter, "y":counter * 2}
        mockHand.handDirection = 1  # ty: ignore[invalid-assignment]
        mockHand.pairWiseDistances = {"thumb_index":5.0 + (counter % 5)}
        mockHand.pairWiseAngles = {"thumb_tip":45.0 + (counter % 10)}

        printer.print_all_data(mockHand)
        counter += 1

        time.sleep(1/30)