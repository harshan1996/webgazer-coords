from flask import Flask,request,Response
import json,threading
from flask_cors import CORS
from random import randint
from time import sleep
from gen_coords import generate_and_add_coords


app=Flask(__name__)
CORS(app)

DELAY=0.1


@app.route("/coord", methods=["POST"])
def coordinates():
    # Making the data persist till the next API call.
    file_paths = ['./data.csv','./result.txt']
    for file_path in file_paths:
        with open(file_path,"w") as file:
                file.truncate()

    # shifted from global scope to local
    terminate_flag = [False]

    data_sent=request.get_json()

    boxes_coords=data_sent[0][:-1]
    # print(boxes_coords)
    end_button_coords_ui=data_sent[0][-1]
    # print(end_button_coords_ui)
    text_in_the_boxes=data_sent[1]
    # print(text_in_the_boxes)

    def send_coordinate():
        continue_stream=True

        count=0

        check_coordinates=list()
        check_end_button_coords=list()

        started_stream=False

        while continue_stream:
            import csv
            # filename = "./coord_samples/sample1.csv"

            # Starting the thread to handle the function to generate and add values to the csv file
            filename="./data.csv"
            if not started_stream:
                print("started")
                started_stream=True
                thread1 = threading.Thread(target=generate_and_add_coords,args=(terminate_flag,))
                thread1.start()
            
            with open(filename, 'r') as data:
                # Seek to the end of the file 
                # comment the below one which is unnecessary for the static csv files
                data.seek(0, 2)
                csvreader = csv.reader(data)
                # print("file reading happening")
                for (idx,coord) in enumerate(csvreader,1):
                    sleep(DELAY)
                    print(idx,"   ",coord)
                    check_coordinates.append(coord)
                    check_end_button_coords.append(coord)
                    # It has to be data only
                    yield f"data: {json.dumps(coord)}\n\n"

                    # TEMPORARY IF BLOCK TO STOP THE CSV VALUES REPETITION for the test cases
                    # Alternative : if coord=="": continue_stream=False
                    if idx==1:
                        count+=1
                        print("count=",count)
                        if count==2:
                            continue_stream=False
                            break

                    # print(len(check_end_button_coords))
                    
                    if len(check_end_button_coords)==20 and ((int(check_end_button_coords[-1][0]) >= int(end_button_coords_ui[0]) and int(check_end_button_coords[-1][0]) <= int(end_button_coords_ui[2])) and (int(check_end_button_coords[-1][1]) >= int(end_button_coords_ui[1]) and int(check_end_button_coords[-1][1]) <= int(end_button_coords_ui[3]))):
                        # print("checked")
                        found_last_coordinate=False
                        for (index,coord) in enumerate(check_end_button_coords[:-1]):
                            if (int(coord[0]) >= int(end_button_coords_ui[0]) and int(coord[0]) <= int(end_button_coords_ui[2])) and (int(coord[1]) >= int(end_button_coords_ui[1]) and int(coord[1]) <= int(end_button_coords_ui[3])):
                                if coord==check_end_button_coords[-2]:

                                    # Stopping the function when condition met
                                    terminate_flag[0] = True
                                    print("THIS IS THE END  ")
                                    yield f"data:{json.dumps(['end',end_button_coords_ui])}\n\n"

                                    # To break the gen_coords function and the current while loop
                                    # found_last_coordinate=True

                        
                                    # FOR STATIC CSV FILE
                                    # found_last_coordinate=True
                                    # yield f"data:{json.dumps([None,end_button_coords_ui])}\n\n"
                                    # break
                            else:
                                check_end_button_coords= check_end_button_coords[index+1:]
                                break

                        if found_last_coordinate:
                            continue_stream = False
                            break

                
                    elif len(check_coordinates) == 10:
                        # print("10 COORDINATES IN THE LIST EXACTLY",check_coordinates)
                        box_of_interest = None
                        for box_coord in boxes_coords:

                            if (int(check_coordinates[-1][0]) >= int(box_coord[0]) and int(
                                    check_coordinates[-1][0]) <= int(box_coord[2])) and (
                                    int(check_coordinates[-1][1]) >= int(box_coord[1]) and int(
                                    check_coordinates[-1][1]) <= int(box_coord[3])):
                                box_of_interest = box_coord
                                break

                        if box_of_interest is not None:
                            
                            for (index,j) in enumerate(check_coordinates[:-1]):

                                if (int(j[0]) >= int(box_of_interest[0]) and int(j[0]) <= int(
                                        box_of_interest[2])) and (
                                        int(j[1]) >= int(box_of_interest[1]) and int(j[1]) <= int(
                                        box_of_interest[3])):
                                    
                                    if j == check_coordinates[-2]:
                                        # data = [[box_coords.index(box_of_interest), box_of_interest],
                                        #         {check_coordinates.index(j): j}]
                                        text_in_the_box=text_in_the_boxes[boxes_coords.index(box_of_interest)]

                                        data = [text_in_the_box,box_of_interest]
                                        check_coordinates.clear()
                                        yield f'data: {json.dumps(data)}\n\n'
                                        with open("result.txt","a") as result:
                                            result.write(text_in_the_box)
                                        break

                                else:
                                    check_coordinates=check_coordinates[index+1:]
                                    # print("check_coordinates in ELSE BLOCK=",check_coordinates)
                                    break
                        else:
                            check_coordinates.clear()

                    if len(check_end_button_coords)==20:
                        check_end_button_coords.clear()

                    if len(check_coordinates)==10:
                        check_coordinates.clear()


    return Response(send_coordinate(), mimetype='text/event-stream')
    
if __name__=='__main__':
    app.run(port=5000,debug=True)