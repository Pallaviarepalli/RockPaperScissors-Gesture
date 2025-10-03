import cv2
from cvzone.HandTrackingModule import HandDetector
import random
import time

# Initialize webcam
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, detectionCon=0.8)

player_score = 0
computer_score = 0
round_time = 2  # seconds to show result

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Detect hands and draw skeleton
    hands, img = detector.findHands(img, draw=True)

    player_gesture = "None"

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        if fingers == [0,0,0,0,0]:
            player_gesture = "Rock"
        elif fingers == [1,1,1,1,1]:
            player_gesture = "Paper"
        elif fingers == [0,1,1,0,0]:
            player_gesture = "Scissors"

        # Computer randomly chooses
        computer_gesture = random.choice(["Rock", "Paper", "Scissors"])

        # Decide winner
        if player_gesture == computer_gesture:
            winner = "Tie"
        elif (player_gesture == "Rock" and computer_gesture == "Scissors") or \
             (player_gesture == "Scissors" and computer_gesture == "Paper") or \
             (player_gesture == "Paper" and computer_gesture == "Rock"):
            winner = "Player Wins"
            player_score += 1
        else:
            winner = "Computer Wins"
            computer_score += 1

        # Show result for a few seconds
        start_time = time.time()
        while time.time() - start_time < round_time:
            success, temp_img = cap.read()
            temp_img = cv2.flip(temp_img, 1)
            detector.findHands(temp_img, draw=True)  # keep hand lines visible

            cv2.putText(temp_img, f'Player: {player_gesture}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.putText(temp_img, f'Computer: {computer_gesture}', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv2.putText(temp_img, f'Winner: {winner}', (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            cv2.putText(temp_img, f'Score - Player: {player_score}  Computer: {computer_score}',
                        (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

            cv2.imshow("Rock Paper Scissors", temp_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Always show score and webcam
    cv2.putText(img, f'Score - Player: {player_score}  Computer: {computer_score}',
                (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
    cv2.imshow("Rock Paper Scissors", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()