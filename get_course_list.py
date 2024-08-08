import csv

def get_all_course_numbers(file_path):
    # 创建一个空字典用于存储科目及其编号
    courses_dict = {}

    # 读取CSV文件
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # 跳过标题行
        for row in csv_reader:
            course_name = row[0]
            # 提取科目代码和编号
            course_code = course_name[:3]
            course_number = course_name[3:]
            if course_code not in courses_dict:
                courses_dict[course_code] = []
            if course_number not in courses_dict[course_code]:
                courses_dict[course_code].append(course_number)
    
    return courses_dict

# 使用示例
file_path = './all_info_modified.csv'  # 确保文件路径正确
courses_dict = get_all_course_numbers(file_path)
print(courses_dict.keys())


# if chosen_subject == 'ACT':
#     chosen_subject = st.selectbox("Choose your favourite course", ACT)
for subject, course_numbers in courses_dict.items():
    print(f"'{subject}': {course_numbers},")

    # print(f"if chosen_subject == '{subject}':\n\tchosen_course = st.selectbox(\"Choose your favourite course\", {subject})")