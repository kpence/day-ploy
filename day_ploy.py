# This is an open-source SuperMemo Plan alternative
# To learn more about SuperMemo Plan, please visit: https://help.supermemo.org/wiki/Plan
# The program is pretty easy to use:
## Enter the list of the activities which you want to do today
## Enter the desired number of minutes which you would like to spend on each of these activities
## Let the program give you a more realistic number of minutes for each of your activities

# * Start

import time
import pandas
import csv
import os
import sys

# * Initialise

daily_mins = int(16*60)

# * Main

# This is a function for adding new tasks to your CSV
def adding():
	while True: # This is just a loop that asks the user to enter the activity name and desired length
		activity_name = input("Enter the name of your activity (enter . to quit adding): ")
		if activity_name == ".":
			break
		else:
			length = int(input("Enter length (in minutes): ")) # This will ask the user for the number of minutes
			
            # TODO might need to make the name of the CSV file change according to the date. But this can be done later: "data.csv" should do for now.
			with open(os.path.join(sys.path[0], 'data.csv'), mode='a', newline='') as csv_file:
				fieldnames = [ # TODO another fieldname which is needed is the start time of each activity (make sure you add it in writer.writerow!)
                    'Fixed',
                    'Rigid',
                    'Activity',
                    'Length',
                    'ActLen',
				]
                
				writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

				writer.writerow({
                    'Activity': activity_name,
                    'Length': length,
                    'ActLen': 0
				})
                
def view_and_update():
    total_length_for_day = daily_mins # TODO get this from the user

    file_path = os.path.join(sys.path[0],'data.csv')
    with open(file_path, newline='') as csvfile:
        rows = [{key: val.strip() for key, val in row.items()} for row in csv.DictReader(csvfile)]

        # TODO validate the csv file has everything needed

        updated_rows = []

        def populate_actual_length_for_segment(segment_rows, segment_start_time, segment_end_time):
            segment_points_total = sum([int(row['Length']) for row in segment_rows])
            segment_ratio_multiplier = float(segment_end_time - segment_start_time) / float(segment_points_total)

            segment_time_remaining = segment_end_time - segment_start_time

            for row in segment_rows[:-1]:
                row['ActLen'] = int(row['Length']) if row['Rigid'] != '' else int(float(row['Length']) * segment_ratio_multiplier)
                segment_time_remaining -= int(row['ActLen'])
                
                # TODO Handle the bugs here
                assert segment_time_remaining > 0, "This plan can't work because thefloat. Ki hasn't decided how to handle this yet, please bug him.";

            segment_rows[-1]['ActLen'] = segment_time_remaining

            return segment_rows

        segment_start_index = 0
        segment_start_time = 0

        for index, row in enumerate(rows):
            assert row['Length'] != '', "There is a row in " + file_path + " that is missing a length value."
            assert int(row['Length']) > 0, "There is a row in " + file_path + " with a non-positive length value."
            if row['Fixed'] != '':
                segment_end_time = int(row['Fixed'])
                assert int(row['Length']) > 0, "There is a Fixed row in " + file_path + " with a non-positive value for Fixed"
                assert int(row['Length']) < total_length_for_day, "There is a Fixed row in " + file_path + " with a value for Fixed that is greater than the total length for the day."
                updated_rows.extend(populate_actual_length_for_segment(rows[segment_start_index:index], segment_start_time, segment_end_time))
                segment_start_time = segment_end_time
                segment_start_index = index

        updated_rows.extend(populate_actual_length_for_segment(rows[segment_start_index:], segment_start_time, total_length_for_day))

    # Prints the new updated table
    pretty_fmt = "{:<8} {:<8} {:<8} {:<8} {:<8}"
    print (pretty_fmt.format("Fixed", "Rigid", "Activity", "Length", "ActLen"))
    for row in updated_rows:
        fixed = row["Fixed"]
        rigid = row["Rigid"]
        activity = row["Activity"]
        length = row["Length"]
        act_len = row["ActLen"]
        print(pretty_fmt.format(fixed, rigid, activity, length, act_len))

def repeater():
    repeat = input("What do you want to do now?\n1. Add tasks\n2. Open the table menu\n3. Close the application\n")
    if repeat == "1":
        adding()
        repeater()
        
    elif repeat == "2":
        view_and_update()
        repeater()

repeater() # My primitive method of looping the program :)
