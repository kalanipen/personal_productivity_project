import time 
import datetime
import tkinter as tk

#variables 

#createe aplication window using tkinter 
root = tk.Tk()  
root.title("clock in clock out")  # Set window title
root.geometry("300x400")  # Set window size
current_time = 0
hourly_wage = 17.0
todays_date = datetime.datetime.now()
 

#functions
def clock_in():
    current_time = time.time() #get first timestamp 
    time_display_area.delete(0,2)
    time_display_area.insert(tk.END, f'clocked in at {current_time}')
    

def clock_out(): 
    current_time = time.time() #get second timestamp 
    time_display_area.insert(tk.END, f'clocked out at {current_time}')
    calc_time() #run the calc for the elapsed time between last in/outs


def calc_time():
    #variables for times in and out 
    times = list(time_display_area.get(0,2))#gets the listings for time input in appbox 
    in_time = times[0]
    out_time = times[1]
    #strip strings for in/out floats
    in_time = float(in_time.strip('clocked in at '))
    out_time = float(out_time.strip('clocked out at '))
    

    #calculations for the worked time total with secs mins hours
    total_elapsed_mins = (out_time - in_time) // 60 
    total_elapsed_secs = (out_time - in_time) % 60
    total_elapsed_hours = total_elapsed_mins // 60
    remaining_mins = total_elapsed_mins % 60

    hours_for_wages = total_elapsed_mins / 60
    #display box write out for the results of the calc and worked time along with writing report to record.txt
    report_statement = (f'clocked in for  '+ 
                       f'{total_elapsed_hours} hours {remaining_mins} minutes'+
                       f' {total_elapsed_secs} seconds {todays_date}')
    
    time_display_area.delete(0,2)
    time_display_area.insert(tk.END, f'{report_statement}')
    
    with open('record.txt', 'a+') as f: #opening record file and writing to it
        f.write(f'\n{report_statement}')


def view_labor():
    current_times = []
    with open('record.txt', 'r') as f:
        current_times = f.readlines() #create list to store the lines in record 

    #containers for the flaots for calcs
    split_wages_whole_hours = []
    split_wages_whole_mins = []

    for a in current_times: #iteration to get the numbers we need from record
        val = a 
        float_hour = val[16:19]
        float_min = val[26:29]
        split_wages_whole_hours.append(float_hour)
        split_wages_whole_mins.append(float_min)

    #converts the strings gained into usable flaots
    split_wages_whole_hours = [(lambda x: float(x))(hours) for hours in split_wages_whole_hours] 
    split_wages_whole_mins = [(lambda x: float(x))(mins) for mins in split_wages_whole_mins]
    
    #finally calculate the totals add together and multiplt by the hourly wage 
    total_hours_pre = sum(split_wages_whole_hours)
    total_mins_pre = sum(split_wages_whole_mins) / 60
    final_wage_total = (total_hours_pre + total_mins_pre) * hourly_wage

    #update the app box with the currenty total report
    time_display_area.delete(0,3)
    time_display_area.insert(tk.END, f'you have worked a total of {total_hours_pre + total_mins_pre} and made' +
                             f'{final_wage_total} dollars')
    



#buttons and text boxes for application in/out
clock_in_button = tk.Button(root,text='Clock in', command=clock_in) 
clock_in_button.pack()

clock_out_button = tk.Button(root, text='Clock out',command=clock_out)
clock_out_button.pack(pady=10)

time_display_area = tk.Listbox(root,width=60,height=30) #text box display declaration
time_display_area.pack(pady=10)

#buttons for self labor report 
view_report = tk.Button(root,text='View Report', command=view_labor)
view_report.pack(pady=10)

#application run loop 
root.mainloop()