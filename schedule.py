import csv
import itertools
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

counter = 1

COURSES = []
my_dict = {
    'Mo':0,
    'Tu':1,
    'We':2,
    'Th':3,
    'Fr':4,
}

my_dict2 = ['Mo', 'Tu', 'We', 'Th', 'Fr']

class Course:
    def __init__(self, course_name:str):
        self.course_name = course_name
        self.Lecs = []
        self.Labs = []
        self.Tuts = []
        self.Lec_intervals = []
        self.Lab_intervals = []
        self.Tut_intervals = []

class Time_interval:
    def __init__(self, begin:int, end:int):
        self.begin = begin
        self.end = end

# data structure representing a record. Each record will have exactly one class_time
class class_time:
    def __init__(self):
        self.time_intervals = []

# processing a record
# return a class_time
def string_to_time(s_time:str, course_name:str, session:str):
    # All possible format:
    # We 20:00 - 20:50
    # Fr 09:30 - 10:20
    # ...
    # TuTh 08:30 - 09:50
    # MoWe 08:30 - 09:50
    # ...
    # We 09:00 - 10:20&We 13:30 - 14:50
    # ...
    classtime = class_time()
    times = s_time.split('&')
    # time: Th 10:30 - 11:50
    for time in times:
        dayAtime = time.split(' ', 1)
        days:str =  dayAtime[0]
        
        time:str = dayAtime[1]
        begin_time = time[0:5]
        end_time   = time[8:13]
        fbegin_time = float(begin_time.replace(':', '.'))
        fend_time   = float(end_time.replace(':', '.'))
        if len(days) > 2:
            day1 = days[0:2]
            day2 = days[2:]
            dAfbegin_time1 = my_dict[day1]*24 + fbegin_time
            dAfend_time1   = my_dict[day1]*24 + fend_time
            time_interval1 = {
            'session':session,
            'name':course_name,
            'begin':dAfbegin_time1,
            'end':dAfend_time1
        }
            classtime.time_intervals.append(time_interval1)
            dAfbegin_time2 = my_dict[day2]*24 + fbegin_time
            dAfend_time2   = my_dict[day2]*24 + fend_time
            time_interval2 = {
            'session':session,
            'name':course_name,
            'begin':dAfbegin_time2,
            'end':dAfend_time2
        }
            classtime.time_intervals.append(time_interval2)

        else:
            fbegin_time = my_dict[days]*24 + fbegin_time
            fend_time   = my_dict[days]*24 + fend_time
            
            time_interval = {
                'session':session,
                'name':course_name,
                'begin':fbegin_time,
                'end':fend_time
            }
            classtime.time_intervals.append(time_interval)
    return classtime


def get_the_course_instance(course_name:str):
    for course in COURSES:
        if course.course_name == course_name:
            return course
    # instance of the course not created
    new_course = Course(course_name)
    COURSES.append(new_course)
    return new_course


def get_course_data_by_name(file_path, courses):
    with open(file_path, "r", newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # 读取表头
        # print("Header:", header)

        # 找到Name列的索引
        name_index = header.index("Name")
        rows = []

        # 遍历所有行，查找匹配的Name
        for row in reader:
            if row[name_index] in courses:
                rows.append(row)
    
    return rows

# compute a list of possible combination of class_time for one course. No validity check for a course
def compute_selection_for_a_course(course:Course):
    selections = []
    # for L_classtime in course.Lec_intervals:
    #     for T_classtime in course.Tut_intervals:
    #         for Lab_classtime in course.Lab_intervals:
    #             selection = class_time()
    #             selection.time_intervals = L_classtime.time_intervals + T_classtime.time_intervals + Lab_classtime.time_intervals
    #             selections.append(selection)
    
    # 检查哪些列表是非空的
    lec_intervals = course.Lec_intervals if course.Lec_intervals else [class_time()]
    tut_intervals = course.Tut_intervals if course.Tut_intervals else [class_time()]
    lab_intervals = course.Lab_intervals if course.Lab_intervals else [class_time()]

    # 使用itertools.product生成所有非空列表的组合
    for L_classtime, T_classtime, Lab_classtime in itertools.product(lec_intervals, tut_intervals, lab_intervals):
        selection = class_time()
        # 合并所有时间段
        selection.time_intervals = L_classtime.time_intervals + T_classtime.time_intervals + Lab_classtime.time_intervals
        # 如果时间段不是全空，才添加到selections
        if selection.time_intervals:
            selections.append(selection)

    return selections

def intervals_overlap(interval1, interval2):
    # 检查两个时间间隔是否重叠
    return not (interval1['end'] <= interval2['begin'] or interval1['begin'] >= interval2['end'])

def is_selection_valid(selection1, selection2):
    # 检查两个selection是否有重叠时间段
    for interval1 in selection1.time_intervals:
        for interval2 in selection2.time_intervals:
            if intervals_overlap(interval1, interval2):
                return False
    return True

def is_combination_valid(current_combination, new_selection):
    # 检查当前组合和新选择之间是否有重叠
    for selection in current_combination:
        if not is_selection_valid(selection, new_selection):
            return False
    return True

def find_valid_combinations(SELECTIONS, current_combination=[], index=0):
    # 递归地查找所有合法的选择组合
    if index == len(SELECTIONS):
        return [current_combination]

    valid_combinations = []
    for selection in SELECTIONS[index]:
        if is_combination_valid(current_combination, selection):
            new_combination = current_combination + [selection]
            valid_combinations.extend(find_valid_combinations(SELECTIONS, new_combination, index + 1))

    return valid_combinations

def num2time(num1:float, num2:float):
    day:int = int(num1/24)
    hour1:float = int(num1)%24
    minute1:float = num1 - int(num1)
    minute1 = round(minute1, 1)
    minutes1 = int(100 * minute1)

    hour2:float = int(num2)%24
    minute2:float = num2 - int(num2)
    minute2 = round(minute2, 1)
    minutes2 = int(100 * minute2)

    Day:str = my_dict2[day]

    return Day + ' ' + str(hour1) + ':' + str(minutes1).zfill(2) + ' - ' + str(hour2) + ':' + str(minutes2).zfill(2)

def draw_schedule(courses):
    global counter
    # 解析课程表数据
    data = []
    for course in courses:
        name, schedule = course.split(": ")
        day, times = schedule.split(" ", 1)
        start_time, end_time = times.split(" - ")
        data.append({"课程": name, "星期": day, "开始时间": start_time, "结束时间": end_time})

    df = pd.DataFrame(data)

    # 将星期转换为数值
    day_mapping = {"Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6}
    df["星期"] = df["星期"].map(day_mapping)

    # 将时间转换为 datetime 格式
    base_date = '2024-01-01 '  # 基准日期
    df["原始开始时间"] = pd.to_datetime(base_date + df["开始时间"])
    df["原始结束时间"] = pd.to_datetime(base_date + df["结束时间"])
    df["开始时间"] = pd.to_datetime(base_date + df["开始时间"])
    df["结束时间"] = pd.to_datetime(base_date + df["结束时间"]).dt.ceil("30T")

    # 创建时间网格
    times = pd.date_range("2024-01-01 08:00", "2024-01-01 20:00", freq="30T")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # 绘制课程表
    fig = go.Figure()

    # 添加时间格子
    for index, row in df.iterrows():
        start_time = row["原始开始时间"].strftime('%H:%M')
        end_time = row["原始结束时间"].strftime('%H:%M')
        day_name = days[row["星期"]]

        # 添加矩形
        fig.add_shape(
            type="rect",
            x0=row["星期"] - 0.4,
            x1=row["星期"] + 0.4,
            y0=row["开始时间"],
            y1=row["结束时间"],
            line=dict(color="RoyalBlue"),
            fillcolor="LightSkyBlue",
            layer="below"  # 将矩形放置在文字下方
        )

        # 添加文本
        fig.add_trace(go.Scatter(
            x=[row["星期"]],
            y=[row["开始时间"] + (row["结束时间"] - row["开始时间"]) / 2],
            text=[f"<b>{row['课程']}<br>{start_time} - {end_time}</b>"],
            mode="text",
            textposition="middle center",
            hoverinfo="none",
            textfont=dict(color="black", size=12, family="Arial")
        ))

    # 设置图表布局
    fig.update_layout(
        title=f"每周课程表{counter}",
        xaxis=dict(
            tickvals=list(range(len(days))),
            ticktext=days,
            title="Day",
            range=[-0.5, 6.5]
        ),
        yaxis=dict(
            tickvals=times,
            ticktext=times.strftime('%H:%M'),
            title="Time",
            autorange="reversed"
        ),
        showlegend=False,
        height=600
    )
    counter+=1

    st.plotly_chart(fig)


def process_query(courses, tut_flag):
    # get_course_data_by_name("./all_info_modified.csv", courses)
    rows = get_course_data_by_name("./all_info_modified.csv", courses)
    fill_the_course_info(rows, tut_flag)
    

    # # test Course...
    # for course in COURSES:
    #     print(f"{course.course_name}:")
    #     print("lecs: ")
    #     lec_count = 0
    #     for lectime in course.Lec_intervals:
    #         print(f"L{lec_count}")
    #         lec_count+=1
    #         for time_interval in lectime.time_intervals:
    #             print(f"begin: {time_interval['begin']}")
    #             print(f"end: {time_interval['end']}")
    #         print()

    #     print("tuts: ")
    #     tut_count = 0
    #     for tuttime in course.Tut_intervals:
    #         print(f"T{tut_count}")
    #         tut_count+=1
    #         for time_interval in tuttime.time_intervals:
    #             print(f"begin: {time_interval['begin']}")
    #             print(f"end: {time_interval['end']}")
    #         print()

    #     print("labs: ")
    #     lab_count = 0
    #     for labtime in course.Lab_intervals:
    #         print(f"Lab{lab_count}")
    #         lab_count+=1
    #         for time_interval in labtime.time_intervals:
    #             print(f"begin: {time_interval['begin']}")
    #             print(f"end: {time_interval['end']}")
    #         print()
    
    SELECTIONS = []
    for course in COURSES:
        SELECTIONS.append(compute_selection_for_a_course(course))
    
    ## is_selection_valid(selection1, selection2) is correct!
    # selection1 = SELECTIONS[0]
    # selection2 = SELECTIONS[1]
    # count = 0
    # for sel1 in selection1:
    #     for sel2 in selection2:
    #         if not is_selection_valid(sel1, sel2):
    #             count+=1
    # print(count)

    all_coms = find_valid_combinations(SELECTIONS)
    schedules = []
    # print(len(all_coms))
    # print()
    # print()
    # print()
    com_count = 1
    for com in all_coms:
        schedule = []
        # print(f"combinition {com_count}: ")
        com_count+=1
        for sel in com:
            for time_interval in sel.time_intervals:
                # print(f"{time_interval['begin']} - {time_interval['end']}")
                # print(f"{time_interval['name']}({time_interval['session']}): {num2time(time_interval['begin'], time_interval['end'])}")
                schedule.append(f"{time_interval['name']}({time_interval['session']}): {num2time(time_interval['begin'], time_interval['end'])}")
        schedules.append(schedule)
        # print()
        # print()
    return schedules

def fill_the_course_info(rows, tut_flag):
    for row in rows:
        course_name = row[0]
        course:Course = get_the_course_instance(course_name)
        session:str = row[1]
        s_time:str = row[2]
        if session.startswith('T'):
            if not tut_flag:
                tut_starttime = int(s_time.split(' ', 1)[1][0:2])
                if tut_starttime >= 19:
                    continue
            if s_time not in course.Tuts:
                course.Tuts.append(s_time)
                # print(s_time)
                course.Tut_intervals.append(string_to_time(s_time, course_name, 'T'))
        elif session.startswith('LAB'):
            if s_time not in course.Labs:
                course.Labs.append(s_time)
                # print(s_time)
                course.Lab_intervals.append(string_to_time(s_time, course_name, 'LAB'))

        elif session.startswith('L') and session[3] == '-':
            if s_time not in course.Lecs:
                course.Lecs.append(s_time)
                # print(s_time)
                course.Lec_intervals.append(string_to_time(s_time, course_name, 'L'))
    


def main():
    # 初始化购物车
    if 'shopping_cart' not in st.session_state:
        st.session_state['shopping_cart'] = []
    
    st.title('Weekly Schedule')
    # # 示例课程表数据
    # courses = [
    #     "BIO2101(T): Fr 9:30 - 10:20",
    #     "BIO2101(LAB): Mo 15:00 - 17:50",
    #     "FIN4231(L): Tu 18:30 - 19:50",
    #     "FIN4231(L): Th 18:30 - 19:50",
    #     "FIN4231(T): Fr 19:00 - 19:50"
    # ]

    # # 调用函数绘制课程表
    # draw_schedule(courses)

    # courses = [
    #     "BIO2101(T): Fr 9:30 - 10:20",
    #     "BIO2101(LAB): Mo 15:00 - 17:50",
    #     "FIN4231(L): Tu 18:30 - 19:50",
    #     "FIN4231(L): Th 18:30 - 19:50",
    #     "FIN4231(T): Fr 20:00 - 20:50"
    # ]

    # draw_schedule(courses)


    # Course Lists:
    course_info = {
        'ACT': ['2111', '2121', '3011', '3141', '3154', '3311', '4111', '4131', '4252', '4253', '4321'],
        'PSY': ['1020', '2020', '2040', '2110', '2120', '2130', '3010', '3110', '3130', '3150', '4010', '4020', '4130', '4180'],
        'BIM': ['2005', '3007', '3008', '3010', '3014', '3020'],
        'BIO': ['1008', '2001', '2002', '2101', '3001', '3002', '3003', '3101', '3214', '3901', '3902', '3903', '3904', '4203', '4901'],
        'BME': ['3001', '3201', '3320', '4006', '4008', '4011', '4012', '4013'],
        'CHM': ['1001', '1002', '1011', '2002', '2110', '2210', '2228', '2310', '2317', '2338', '3420', '3530', '4330'],
        'CHI': ['1000', '2010'],
        'CLC': ['1101', '1201', '1301', '1401'],
        'CEC': ['1000', '2000', '3000', '4000'],
        'CSC': ['1001', '1003', '1005', '3001', '3002', '3050', '3100', '3150', '3160', '3170', '3185', '4005', '4160'],
        'DDA': ['2081', '2082', '2083', '3005', '3010', '3020', '3600', '4002', '4100', '4230', '4250', '4260', '4340'],
        'DMS': ['2030'],
        'ECO': ['2011', '2021', '3080', '3110', '3121', '3160', '3211', '3430', '3470', '3480', '3710', '4121'],
        'ECE': ['1810', '3001', '3050', '3060', '3080', '3200', '3201', '3810', '4016'],
        'EIE': ['2001', '3510', '4003', '4007'],
        'ENE': ['3004', '3050', '4003', '4005', '4008'],
        'ENG': ['1001', '2001', '3101'],
        'ENB': ['2001', '2002', '2004', '3002', '3004', '3005', '4101', '4102', '4103', '4201', '4203', '4208', '4302', '4308'],
        'ENL': ['1001', '1003'],
        'FIN': ['2010', '3080', '3210', '3380', '4060', '4110', '4120', '4210', '4231'],
        'FRN': ['1001'],
        'GEA': ['2000'],
        'GEB': ['2109', '2203', '2205', '2206', '2301', '2404', '2405', '2503', '2601', '3301', '3302'],
        'GEC': ['2002', '2109', '2110', '2112', '2205', '2206', '2207', '3109', '3111', '3112', '3203', '3401', '3402', '3405', '3407', '3410'],
        'GED': ['2003', '2107', '2110', '2113', '2119', '2121', '2122', '2123', '2124', '2302', '3308'],
        'GFH': ['1000'],
        'GFN': ['1000'],
        'ERG': ['1000', '2081', '2082', '2083', '4100', '4901'],
        'GLB': ['1030', '3060'],
        'HSS': ['1004', '1006', '1009'],
        'IBA': ['4007'],
        'ITE': ['1000'],
        'IDE': ['3005', '4110'],
        'JAP': ['1001'],
        'KOR': ['1001'],
        'LIT': ['2100', '3001'],
        'MGT': ['3010', '3070', '3210', '3250', '3260', '4020', '4030', '4080', '4187', '4188', '4210', '4250', '4270'],
        'MIS': ['2051'],
        'MKT': ['2010', '3020', '3080', '3320', '4040', '4110', '4120', '4150', '4220'],
        'MSE': ['3013', '4005'],
        'MAT': ['1001', '1005', '1011', '2001', '2040', '2050', '2060', '3004', '3006', '3007', '3040', '3042', '3280', '3300', '4033', '4220', '4500'],
        'MED': ['1001', '1011', '1021', '1031', '1100', '1200', '2001', '2011', '2050', '2100', '3001', '3002', '3003', '3011', '3020', '3021', '3031', '3100', '3200', '3300', '4010', '4011', '4012', '4013', '4100', '4200'],
        'MUS': ['1001', '1003', '1004', '1005', '1007', '1010', '1110', '1150', '1200', '1605', '2001', '2004', '2005', '2007', '2010', '2021', '2023', '2025', '2112', '2200', '2328', '2333', '2350', '2501', '2603', '2610', '2612', '2703', '2802', '3001', '3007', '3010', '3110', '3112', '3201', '3212', '3221', '3333', '3501', '3533', '3700', '3800', '4001', '4007', '4017', '4111', '4501', '4506', '4611'],
        'PHM': ['2004', '2006', '2010', '3002', '3003', '3017', '4003'],
        'PED': ['1001'],
        'PHY': ['1002', '1010', '1210', '2020', '2610', '3006', '3110', '3210', '3230', '3240', '3310', '3410', '3810', '3950', '4001'],
        'SPN': ['1001'],
        'STA': ['2001', '2002', '2003', '3001', '4001', '4003', '4020', '4042', '4606'],
        'TRA': ['1010', '2010', '2130', '2320', '3010', '3110', '3220', '3240', '3250', '3260', '3280', '3310', '4030'],
        'URM': ['2010', '2040']
    }
    

    st.subheader("Choose your Course")
    subjects = ['Choose Subject', 'ACT', 'PSY', 'BIM', 'BIO', 'BME', 'CHM', 'CHI', 'CLC', 'CEC', 'CSC', 'DDA', 'DMS', 'ECO', 'ECE', 'EIE', 'ENE', 'ENG', 'ENB', 'ENL', 'FIN', 'FRN', 'GEA', 'GEB', 'GEC', 'GED', 'GFH', 'GFN', 'ERG', 'GLB', 'HSS', 'IBA', 'ITE', 'IDE', 'JAP', 'KOR', 'LIT', 'MGT', 'MIS', 'MKT', 'MSE', 'MAT', 'MED', 'MUS', 'PHM', 'PED', 'PHY', 'SPN', 'STA', 'TRA', 'URM']
    chosen_subject = st.selectbox("Choose your favourite subject", subjects)
    if chosen_subject == subjects[0]:
        st.warning("Please Choose the Subject")
    else:
        chosen_course = st.selectbox("Choose your course", course_info[chosen_subject])
        if st.button("Add to Cart"):
            CourseCode = f"{chosen_subject}{chosen_course}"
            if CourseCode not in st.session_state['shopping_cart']:
                st.session_state['shopping_cart'].append(CourseCode)
                st.success(f"Added {CourseCode} to cart")
            else:
                st.warning(f"{CourseCode} is already in the cart")

    # 显示购物车内容
    if st.session_state['shopping_cart']:
        for course in st.session_state['shopping_cart']:
            if st.button(f"Remove {course} from cart", key=course):
                st.session_state['shopping_cart'].remove(course)
                st.success(f"Removed {course} from cart")
    else:
        st.write("Your cart is empty.")
    
    # 显示当前购物车内容
    st.subheader("Shopping Cart")
    st.write("", st.session_state['shopping_cart'])


    tut_flag = st.checkbox("uncheck to ignore tuts after 19:00")

    # 初始化滑动条值和 schedules
    if 'slider_value' not in st.session_state:
        st.session_state['slider_value'] = 1
    if 'schedules' not in st.session_state:
        st.session_state['schedules'] = []

    # Apply Button
    if st.button('Apply'):

        schedules = process_query(st.session_state['shopping_cart'], tut_flag)
        st.session_state['schedules'] = schedules  # 保存生成的 schedules
        st.session_state['slider_value'] = 1  # 重置 slider 值
        

    
      # 如果存在 schedules 则显示滑动条和 schedules
    if st.session_state['schedules']:
        
        # 用户控制展示多少 schedule
        no_of_scheds = st.slider('Number of schedules', 0, len(st.session_state['schedules']), 0)
        
        
        st.write(f"There are {len(st.session_state['schedules'])} possible schedules, showing {no_of_scheds} of them")
        st.write(f"drawing the schedule may take some time...")
        # 显示 schedule
        c = 0
        for sched in st.session_state['schedules']:
            if c >= no_of_scheds:
                break
            draw_schedule(sched)
            c += 1

main()
