# [Tuts+]() Video Downloader

NOTE: To download premium videos, you're required to have a tuts+ premium account.



## REQUIREMENTS

[youtube-dl](https://github.com/rg3/youtube-dl)

python 3.x

	pip install -r requirements.txt

## USAGE

**Step1:** Edit `config.py` and replace `your username here` and `your password here` with your own.

**Step2:** Edit `cookies.txt` and copy and paste tuts+ site's cookie.
To copy the cookie, I used [cookies.txt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg?hl=en), a chrome extension.

**Step3:** Excute the command below.

	python dl.py [OPTIONS]

## OPTIONS

	--category		tuts+ category (default: code)
					it'll be shown as a subdomain of tutsplus.com
					e.g. code.tutsplus.com

	--slug			tuts+ course slug (default: None)
			  		it'll be shown as its url.
					e.g. when url is something like this: https://code.tutsplus.com/courses/javascript-without-jquery,
					then slug is `javascript-without-jquery`

	--directory		directory where videos will be added
					e.g. ~/Desktop/tutsplus

	--page			a starting page number

## EXAMPLES

Download all courses in code category

	python dl.py

Download a specific course in code category

	python dl.py --slug javascript-without-jquery

Download all courses in a specific category, then

	python dl.py --category design

Download a specific course in a specific category, then

	python dl.py --category code --slug get-started-with-nativescript-and-mobile-angular-2

Download all courses in a specific category from a specific page into a specific directory
	
	python dl.py --category design --page 3 --directory ~/Desktop/tutsplus


## OUTPUT

Downloaded videos will be stored in
 `./videos/CATEGORY_NAME/COURSE_NAME/INDEX - LESSON_NAME.[ext]`

e.g. `./videos/code/javascript-without-jquery/00001 - Introduction.mp4`
