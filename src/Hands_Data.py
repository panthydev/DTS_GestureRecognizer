from hand import Hand
import HandDirection

class HandsData:
    def __init__(self):
        RightHand = Hand()
        LeftHand = Hand()
        self.HandsDictionary : dict[str, Hand] = {"Right" : RightHand, "Left" : LeftHand}


    def UpdateDirections(DetectionResults, HandsData : HandsData):

        for i in range(len(DetectionResults.handedness)):

            handDirection = DetectionResults.handedness[i].display_name
            
            HandsData.HandsDictionary[handDirection].handDirection = handDirection 

            HandsData.HandsDictionary[handDirection].rawPositions = DetectionResults.hand_landmarks[i]
                     
         
                
                        

    
