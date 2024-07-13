import csv, heapq


class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Category({self.id}, {self.name})"


class School:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"School({self.id}, {self.name})"


class Course:
    def __init__(
        self, id: int, school: int, category: int, title: str, rate: int, length: int
    ):
        self.id = id
        self.school = school
        self.category = category
        self.title = title
        self.rate = rate
        self.length = length


def load_course_from_row(row: list[str]) -> Course:
    return Course(
        int(row[0]), int(row[1]), int(row[2]), row[3], int(row[4]), int(row[5])
    )


def load_category_from_row(row: list[str]) -> Category:
    return Category(int(row[0]), row[1])


def load_school_from_row(row: list[str]) -> School:
    return School(int(row[0]), row[1])


with open("category.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    categories = {}
    for row in reader:
        category = load_category_from_row(row)
        categories[category.id] = category

with open("schools.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    schools = {}
    for row in reader:
        school = load_school_from_row(row)
        schools[school.id] = school

max_course_id = -1
category_heaps = {}
category_to_courses = {}

def load_course_into_memory(course: Course):
    global max_course_id, category_heaps, category_to_courses
    
    if course.category not in category_heaps:
        category_heaps[course.category] = []
        category_to_courses[course.category] = []

    heapq.heappush(
        category_heaps[course.category], (-course.rate, course.id, course)
    )
    category_to_courses[course.category].append(course)

    if course.id > max_course_id:
        max_course_id = course.id

with open("courses.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        course = load_course_from_row(row)
        load_course_into_memory(course)


def ask_category_n() -> tuple[int, int]:
    for category in categories:
        print(f"{category}: {categories[category]}")

    cat = int(input("请输入要查看的课程分类："))
    n = int(input("请输入要查看的课程数量："))

    return cat, n

def ask_school_n() -> tuple[int, int]:
    for school in schools:
        print(f"{school}: {schools[school]}")

    school = int(input("请输入要查看的学校："))
    n = int(input("请输入要查看的课程数量："))

    return school, n

def top_n_by_category():
    cat, n = ask_category_n()

    if cat not in categories:
        print("无此课程分类")
        return

    print(f"分类：{categories[cat]}")

    heap_copy = list(category_heaps[cat])

    for i in range(n):
        if len(heap_copy) == 0:
            break

        rate, course_id, course = heapq.heappop(heap_copy)
        print(
            f"[{course.id}] {schools[course.school].name} {course.title} 评分{course.rate}分 {course.length}分钟"
        )

def top_n_by_school():
    school, n = ask_school_n()

    if not school in schools:
        print("无此学校")
        return
    
    print(f"学校：{schools[school]}")

    school_courses = []
    for courses in category_to_courses.values():
        for course in courses:
            if course.school == school:
                heapq.heappush(school_courses, (-course.rate, course.id, course))
    
    for i in range(n):
        if len(school_courses) == 0:
            break

        rate, course_id, course = heapq.heappop(school_courses)
        print(
            f"[{course.id}] {categories[course.category].name} {course.title} 评分{course.rate}分 {course.length}分钟"
        )

def search_by_keyword():
    keywords = input("请输入关键词，以空格分割：").split()

    matches = []
    for courses in category_to_courses.values():
        for course in courses:
            match_count = 0

            for kw in keywords:
                if kw in course.title:
                    match_count += 1
            
            if match_count > 0:
                heapq.heappush(matches, (-match_count, -course.rate, course.id, course))
    
    for i in range(50):
        if len(matches) == 0:
            break

        match_count, rate, course_id, course = heapq.heappop(matches)
        print(
            f"[{course.id}] {schools[course.school].name} {categories[course.category].name} {course.title} 评分{course.rate}分 {course.length}分钟"
        )

def add_course():
    for school in schools:
        print(f"{school}: {schools[school]}")
    school = int(input("请输入学校编号："))
    if school not in schools:
        print("无此学校")
        return
    
    for category in categories:
        print(f"{category}: {categories[category]}")
    category = int(input("请输入课程分类编号："))
    if category not in categories:
        print("无此课程分类")
        return
    
    title = input("请输入课程名称：")
    if not title:
        print("课程名称不能为空")
        return
    rate = int(input("请输入课程评分："))
    if rate < 0 or rate > 100:
        print("评分应在0-100之间")
        return
    length = int(input("请输入课程时长（分钟）："))
    if not length > 0:
        print("时长应为正整数")
        return
    
    course_id = max_course_id + 1
    course = Course(course_id, school, category, title, rate, length)
    load_course_into_memory(course)

    print("课程添加成功")
    


def main_menu():
    while True:
        print("=== 主菜单 ===")
        print("1. 按分类查看课程（评分最高）")
        print("2. 按学校查看课程（评分最高）")
        print("3. 搜索课程")
        print("4. 新增课程")
        print("0. 退出")

        choice = input("请输入选项：")
        if choice == '1':
            top_n_by_category()
        elif choice == '2':
            top_n_by_school()
        elif choice == '3':
            search_by_keyword()
        elif choice == '4':
            add_course()
        elif choice == '0':
            break
        else:
            print("无效选项")


main_menu()
