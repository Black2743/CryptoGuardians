import cv2
import json
import torch
from datetime import datetime


def main():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/black/Desktop/CryptoGuardians/detectSystem/best.pt', force_reload=False)
    classes = model.names
   
   # cap = cv2.VideoCapture("udp://127.0.0.1:9998")
    cap = cv2.VideoCapture("/home/black/Desktop/CryptoGuardians/source/Suspect_1.mp4")

    while True:
        ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = detecting(frame, model=model)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = color_box(res, frame, classes=classes)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break   
            #cv2.imshow("Video Frame", frame)
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


def bufferJson(alert:{}):
     USERS_FILE="/home/black/Desktop/CryptoGuardians/detectSystem/telegramBot/buffer.json"
     with open(USERS_FILE, "w") as users_file:
            json.dump(alert,users_file)

def detecting (frame, model):
    frame = [frame]
    res = model(frame)
    labels, cords = res.xyxyn[0][:, -1], res.xyxyn[0][:, :-1]
    return labels, cords


def color_box(results, frame, classes, acc=0.82):
    labels, cords = results
    n = len(labels)
    x_window, y_window = frame.shape[1], frame.shape[0]

    for i in range(n): #processing of detected objects
        cords_list = cords[i]
        if cords_list[4] >= acc: 
            print(f"Creating color box . . .")
            x1 = int(cords_list[0]*x_window)
            y1 = int(cords_list[1]*y_window)
            x2 = int(cords_list[2]*x_window)
            y2 = int(cords_list[3]*y_window)
            text_d = classes[int(labels[i])]
            
            now = datetime.now()
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            _alert = {
                "camera_name": "Camera1",
                "location": "Camera1_location",
                "time": formatted_time,
                "photo": f"/home/black/Desktop/CryptoGuardians/detectSystem/telegramBot/savedFrame/{formatted_time}.jpg",
                "incident":text_d
            }
           
            bufferJson(_alert)
            print("*" * 30)
            color = (0, 0, 0)
            if text_d == "pistol":
                color = (255, 0, 0)
            elif text_d == "machine_gun":
                color = (255, 170, 0)
            elif text_d == "knife":
                color = (0, 170, 127)
            else:
                color = (85, 0, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2) #object box
            cv2.rectangle(frame, (x1, y1-20), (x2, y1), color, -1) #text box
            cv2.putText(frame, text_d + f" {round(float(cords_list[4]),2)}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2) #text adding
            cv2.imwrite(_alert["photo"], frame)
            return frame
    return frame

if __name__ == "__main__":
    main()