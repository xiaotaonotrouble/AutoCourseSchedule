# test Course...
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