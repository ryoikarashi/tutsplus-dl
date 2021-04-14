from bs4 import BeautifulSoup
import requests
import os
from time import sleep
from youtube_dl import YoutubeDL
from argparse import ArgumentParser
from config import ACCOUNT

def parse_args():
    # parse command arguments
    # --category: category to download
    # --slug: a course slug to download
    parser = ArgumentParser()
    parser.add_argument('--category', help='specify a category (default: code)')
    parser.add_argument('--slug', help='specify a slug to download a course with the specified slug')
    parser.add_argument('--directory', help='specify a directory where downloaded videos will be added')
    parser.add_argument('--page', help="specify a starting page number")
    args = parser.parse_args()

    # if category is not specified, make default category 'code'
    args.category = args.category or 'code'

    # if directory is not specified, make default directory 'current directory (./)'
    args.directory = args.directory or './'

    # if directory's last character contains '/', then remove it
    args.directory = args.directory[:-1] if args.directory[-1] == '/' else args.directory

    # if page is not specified, make default page number '1'
    args.page = args.page or 1

    return args

args = parse_args()

class TutsplusDownLoader:

    def __init__(self, category=args.category, course_slug=args.slug):
        self.category = category
        self.course_slug = course_slug
        self.directory = args.directory
        self.page_num = int(args.page) - 1
        self.base_url = 'https://' + category + '.tutsplus.com'
        self.url      = self.base_url + '/courses'
        self.certain_course_url = (self.url + '/' + self.course_slug) if self.course_slug else None

    def print_current_page(self, current_page):
        print('----------------------------------------------')
        print('Current Page: ' + current_page)
        print('----------------------------------------------')

    def get_soup(self, url=None, page=None):
        page = str(page)
        url = url or self.url
        request_url = (url + '?page=' + page) if page else url
        result = requests.get(request_url)
        c = result.content
        return BeautifulSoup(c, 'lxml')

    def get_last_page_num(self, base_soup):
        return int(base_soup.select('.pagination__button')[-2].getText())

    def get_course(self, page_soup, index):
        return page_soup.select('.posts__post')[index]

    def get_course_url(self, course):
        return course.select_one('.posts__post-preview')['href']

    def get_num_of_courses(self, page_soup):
        courses = page_soup.select('.posts__post')
        return len(courses)

    def get_course_title(self, course_soup):
        return course_soup.select_one('.content-banner__title').getText()

    def print_course_title(self, course_title):
        print('\t----------------------------------------------')
        print('\tCourse Title: ' + course_title)
        print('\t----------------------------------------------')

    def get_lesson(self, course_soup, index):
        return course_soup.select('h3.lesson-index__lesson')[index]

    def get_lesson_url(self, lesson):
        return lesson.select_one('.lesson-index__lesson-link')['href']

    def get_lesson_title(self, lesson):
        return lesson.select_one('.lesson-index__lesson-title').getText()

    def print_lesson_title(self, lesson_title):
        print('\t\tLesson Title: ' + lesson_title)

    def get_num_of_lessons(self, course_soup):
        lessons = course_soup.select('h3.lesson-index__lesson')
        return len(lessons)

    def get_directory_name(self, course_title):
        return self.directory + '/videos/' + self.category + '/' + course_title

    def create_directory(self, course_title):
        directory = self.get_directory_name(course_title)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def download_via_youtube_dl(self, course_title, lesson_url_list):
        ydl_opts = {
            'username': ACCOUNT['username'],
            'password': ACCOUNT['password'],
            'cookiefile': './cookies.txt',
            'verbose': 'true',
            # add -4 option to avoid HTTP Error 429 Too Many Requests
            # Ref: https://github.com/rg3/youtube-dl/issues/5138
            'force-ipv4': 'true',
            'outtmpl': self.get_directory_name(course_title) + '/%(autonumber)s - %(title)s.%(ext)s'
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(lesson_url_list)

    def download(self):
        # request a specific course page, and get its soup
        print(self.certain_course_url)
        course_soup = self.get_soup(self.certain_course_url)

        # get num of lessons
        num_of_lessons = self.get_num_of_lessons(course_soup)

        # display course info
        course_title = self.get_course_title(course_soup)
        self.print_course_title(course_title)

        lesson_url_list = []

        # loop through lessons in a course
        for k in range(num_of_lessons):

            # get a lesson url
            lesson = self.get_lesson(course_soup, k)
            lesson_url = self.get_lesson_url(lesson)

            # add a lesson url to lesson url list
            lesson_url_list.append(self.base_url + lesson_url)

            # display lesson info
            lesson_title = self.get_lesson_title(lesson)
            self.print_lesson_title(lesson_title)

        # create course-named directory if not created yet
        self.create_directory(course_title)

        # download lessons via youtube_dl
        self.download_via_youtube_dl(course_title, lesson_url_list)


    def downloadAll(self):
        # get html source
        base_soup = self.get_soup()

        # get last page number
        last_page = self.get_last_page_num(base_soup)

        # loop until last page
        for i in range(self.page_num, last_page):

            # display current page number
            current_page = str(i + 1)
            self.print_current_page(current_page)

            # request with a paga number, and get its soup
            page_soup = self.get_soup(self.url, i + 1)

            # get num of courses in a page
            num_of_courses = self.get_num_of_courses(page_soup)

            # loop through courses in a  page
            for j in range(num_of_courses):

                # get a course url
                course = self.get_course(page_soup, j)
                course_url = self.get_course_url(course)

                # request a specific course page, and get its soup
                course_soup = self.get_soup(course_url)

                # get num of lessons
                num_of_lessons = self.get_num_of_lessons(course_soup)

                # display course info
                course_title = self.get_course_title(course_soup)
                self.print_course_title(course_title)

                # create a list to store lessons' url
                lesson_url_list = []

                # loop through lessons in a course
                for k in range(num_of_lessons):

                    # get a lesson url
                    lesson = self.get_lesson(course_soup, k)
                    lesson_url = self.get_lesson_url(lesson)

                    # add a lesson url to lesson url list
                    lesson_url_list.append(self.base_url + lesson_url)

                    # display lesson info
                    lesson_title = self.get_lesson_title(lesson)
                    self.print_lesson_title(lesson_title)

                # create course-named directory if not created yet
                self.create_directory(course_title)

                # download lessons via youtube_dl
                self.download_via_youtube_dl(course_title, lesson_url_list)


# create an instance
downloader = TutsplusDownLoader()

# if a certain course title (course slug) is given as an argument, then download its all lesson videos,
# otherwise download all videos in the specified category
if downloader.course_slug:
    downloader.download()
else:
    downloader.downloadAll()
