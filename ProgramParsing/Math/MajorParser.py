"""
CourseParser.py is a library built to receive information on Major Requirements

Contributors:
Hao Wei Huang
Calder Lund
"""

from bs4 import BeautifulSoup
from ProgramParsing.Math.MajorReq import MathMajorReq
from ProgramParsing.ProgramParser.MajorParser import MajorParser
from StringToNumber import StringToNumber
import re
import pkg_resources


class MathMajorParser(MajorParser):
    def _get_program(self):
        program = self.data.find_all("span", id="ctl00_contentMain_lblBottomTitle")

        if program:
            program = program[0].contents[0].string
        else:
            #Exception for Table II data
            return "Table II"
        #Parsing the heading above the highlighted span
        #if major == degree req, spcialization, parse the highlighted span

        if "requirements" in program.lower() or "specializations" in program.lower() or "specialization" in program.lower():
            program = self.data.find_all("span", class_="pageTitle")
            program = str(program[0].contents[0])

        if "Overview and Degree Requirements" in program:
            program = program.replace(" Overview and Degree Requirements", "")

        #check for minor
        minor = self.data.find_all("span", class_="pageTitle")
        minor = str(minor[0].contents[0])

        if "minor" in str(minor).lower():
            program = minor

        return program
        # TODO: Need a case where this tile area is Degree Requirements

    def _require_all(self, list, major, relatedMajor, additional=None):
        for l in list:
            self.requirement.append(MathMajorReq([l], "All of", major, relatedMajor, self.additionalRequirement, 0))

    def _course_list(self, info, i, oneOf = False):
        list = []
        while i < len(info):

            line = info[i].strip().replace(" to ", "-")

            #Table II exception a bit hardcoded (info[i] == " ")
            if line.startswith("Note") or line.startswith("(") or info[i] == "        ":
                i += 1
                continue

            #check if line is additional course
            # and list make sure theres at least one item in the 1,2,3, of
            if len(line.split(" ")) >= 2 and line.split(" ")[1] == "additional" and list:
                break

            rangeCourse = re.findall(r"[A-Z]+\s{0,1}[1-9][0-9][0-9]\s{0,1}-\s{0,1}[A-Z]+\s{0,1}[1-9][0-9][0-9]",
                                 line)
            courses = re.findall(r"\b[A-Z]{2,10}\b \b[0-9]{1,4}[A-Z]{0,1}\b", line)


            if rangeCourse:
                #TODO: Account for range CS 123-CS 345, excluding CS XXX
                if oneOf:
                    for c in rangeCourse:
                        list.append(c)
                else: list.append(" or ".join(rangeCourse))
                i += 1
                continue

            if not courses and list:
                # List has ended
                break

            if courses:
                if oneOf:
                    for c in courses:
                        list.append(c)
                else: list.append(" or ".join(courses))
            i += 1
        return i, list

    def _additional_list(self, info, i, multiLine):
        list = []
        if multiLine:
            #"Two additional courses from"
            i += 1 #skip first line
            while i < len(info):
                line = info[i].strip().replace(" to ", "-")
                foundPattern = False
                if "additional" in line:
                    break #search is over
                if line.startswith("Note") or line.startswith("("):
                    i += 1
                    continue

                ignoreCourses = [] #To prevent duplicate of ABC XXX-DEF XXX from single regex

                # range CS 389-CS 495
                courses = re.findall(r"[A-Z]+\s{0,1}[1-9][0-9][0-9]\s{0,1}-\s{0,1}[A-Z]+\s{0,1}[1-9][0-9][0-9]",
                                     line)
                if courses:
                    foundPattern = True
                    for course in courses:
                        course = course.strip("\n").strip("\r\n")
                        if not str(course).startswith("("):
                            list.append(course)
                            c = course.split("-")
                            for item in c:
                                item = item.strip()
                                ignoreCourses.append(item)
                else:
                    # find for another match cs 300-
                    maj = ""
                    match = self._getLevelCourses(str(line))

                    for word in line.split(' '):
                        if word.isupper() or "math" in word:  # special case for "One additional 300- or 400-level math course.
                            maj = word.strip("\n").strip("\r\n").upper()
                            break
                    if maj.startswith("(") or maj.startswith("Note"):
                        print("No Major Found")
                        #Do nothing
                    elif match:
                        foundPattern =True
                        for m in match:
                            course = m.strip("\n")
                            course = course.strip("\r\n")
                            list.append(maj + " " + course)
                            #add CS 300- to ignore list for regex
                            course = course.replace("-", "")
                            ignoreCourses.append(maj + " " + course)

                # regular CS 135
                courses = re.findall(r"\b[A-Z]{2,10}\b \b[0-9]{1,4}[A-Z]{0,1}\b", line)
                #to find courses that says excluding CO 480
                exclude = re.findall(r"excluding \b[A-Z]{2,10}\b \b[0-9]{1,4}[A-Z]{0,1}\b", line)
                if exclude:
                    excludeCourse = exclude[0].replace("excluding ", "") #take course code
                    ignoreCourses.append(excludeCourse)
                if courses: foundPattern = True
                for course in courses:
                    if course not in ignoreCourses:
                        list.append(course)


                if not foundPattern and list:
                    # List has ended
                    break
                i += 1

        else:
            line = info[i].strip().replace(" to ", "-")
            i += 1

            ignoreCourses = []  # To prevent duplicate of ABC XXX-DEF XXX from single regex

            #range CS 389-CS495
            courses = re.findall(r"[A-Z]+\s{0,1}[1-9][0-9][0-9]\s{0,1}-\s{0,1}[A-Z]+\s{0,1}[1-9][0-9][0-9]",line)
            if courses:
                for course in courses:
                    course = course.strip("\n").strip("\r\n")
                    if not str(course).startswith("("):
                        list.append(course)
                        c = course.split("-")
                        for item in c:
                            item = item.strip()
                            ignoreCourses.append(item)
            else:
                # find for another match cs 300-
                maj = ""
                match = self._getLevelCourses(str(line))

                for word in line.split(' '):
                    if word.isupper() or "math" in word:  # special case for "One additional 300- or 400-level math course.
                        maj = word.strip("\n").strip("\r\n").upper()
                        break

                if match:
                    for m in match:
                        course = m.strip("\n")
                        course = course.strip("\r\n")
                        list.append(maj + " " + course)
                        # add CS 300- to ignore list for regex
                        course = course.replace("-", "")
                        ignoreCourses.append(maj + " " + course)
                elif maj:
                    list.append(maj)  # Only indicate major but not level
                else:
                    #Four additional elective courses
                    list.append("Elective")

            # regular CS 135
            courses = re.findall(r"\b[A-Z]{2,10}\b \b[0-9]{1,4}[A-Z]{0,1}\b", line)
            # to find courses that says excluding CO 480
            exclude = re.findall(r"excluding \b[A-Z]{2,10}\b \b[0-9]{1,4}[A-Z]{0,1}\b", line)
            if exclude:
                excludeCourse = exclude[0].replace("excluding ", "")  # take course code
                ignoreCourses.append(excludeCourse)
            for course in courses:
                if course not in ignoreCourses:
                    list.append(course)

        return i, list

    def is_additional(self, string):
        string = str(string).lower()
        if "recommended" in string:
            return False
        try:
            secondWord = str(string).split(" ")[1]
        except:
            return False
        if "additional" == secondWord:
            return True
        else: 
            return False

    def load_file(self, file):
        """
                Parse html file to gather a list of required courses for the major

                :return:
        """
        html = pkg_resources.resource_string(__name__, file)
        # html = open(file, encoding="utf8")
        self.data = BeautifulSoup(html, 'html.parser')

        program = self._get_program()

        # find the major related to specializations and options
        relatedMajor = self._get_relatedMajor(program)

        # Find all additional requirement
        self.additionalRequirement = self.getAdditionalRequirement()

        try:
            information = self.data.find("span", {'class': 'MainContent'}).get_text().split("\n")
        except:
            #Table II exception
            information = self.data.find("body").get_text().split("\n")

        i = 0
        while i < len(information):
            if information[i].strip().lower().startswith("one of"):
                i, list = self._course_list(information, i, True)
                self.requirement.append(MathMajorReq(list, "One of", program, relatedMajor, self.additionalRequirement))
            elif information[i].strip().lower().startswith("two of"):
                i, list = self._course_list(information, i)
                self.requirement.append(MathMajorReq(list, "Two of", program, relatedMajor, self.additionalRequirement))
            elif information[i].strip().lower().startswith("three of"):
                i, list = self._course_list(information, i)
                self.requirement.append(MathMajorReq(list, "Three of", program, relatedMajor, self.additionalRequirement))
            elif information[i].strip().lower().startswith("four of"):
                i, list = self._course_list(information, i)
                self.requirement.append(MathMajorReq(list, "Four of", program, relatedMajor, self.additionalRequirement))
            elif information[i].strip().lower().startswith("five of"):
                i, list = self._course_list(information, i)
                self.requirement.append(MathMajorReq(list, "Five of", program, relatedMajor, self.additionalRequirement))
            elif information[i].strip().lower().startswith("six of"):
                i, list = self._course_list(information, i)
                self.requirement.append(MathMajorReq(list, "Six of", program, relatedMajor, self.additionalRequirement))
            elif information[i].strip().lower().startswith("seven of"):
                i, list = self._course_list(information, i)
                self.requirement.append(MathMajorReq(list, "Seven of", program, relatedMajor, self.additionalRequirement))
            elif information[i].strip().lower().startswith("eight of"):
                i, list = self._course_list(information, i)
                self.requirement.append(MathMajorReq(list, "Eight of", program, relatedMajor, self.additionalRequirement))
            elif information[i].strip().lower().startswith("nine of"):
                i, list = self._course_list(information, i)
                self.requirement.append(MathMajorReq(list, "Nine of", program, relatedMajor, self.additionalRequirement))
            elif information[i].strip().lower().startswith("all of"):
                i, list = self._course_list(information, i, True)
                self._require_all(list, program, relatedMajor)
            elif (self.is_additional(information[i]) or self._stringIsNumber(information[i])) \
                    and "excluding the following" not in information[i]: #Three 400- Level courses
                number_additional_string = information[i].lower().split(' ')[0]
                number_additional = StringToNumber[number_additional_string].value
                if not isinstance(number_additional, int):
                    number_additional = number_additional[0]
                #check if one sentence are multiple
                if "." in information[i]:
                    i, list = self._additional_list(information, i, False)
                else:
                    i, list = self._additional_list(information, i, True)
                # need to check if number_additional is an INT
                self.requirement.append(MathMajorReq(list, "Additional", program, relatedMajor, self.additionalRequirement, number_additional))
            else:
                i += 1