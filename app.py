from flask import Flask
import bs4 as bs
import requests
import pandas as pd
import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

def render(source_html):

    import sys
    from PyQt5.QtCore import QEventLoop
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebEngineWidgets import QWebEngineView

    class Render(QWebEngineView):
        def __init__(self, html):
            self.html = None
            self.app = QApplication(sys.argv)
            QWebEngineView.__init__(self)
            self.loadFinished.connect(self._loadFinished)
            self.setHtml(html)

            while self.html is None:
                self.app.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)
            self.app.quit()

        def _callable(self, data):
            self.html = data

        def _loadFinished(self, result):
            self.page().toHtml(self._callable)

    return Render(source_html).html

class Client(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = None
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('load finished!')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

# create flask app
app = Flask(__name__)
app.config.from_object('config.DevelopementConfig')


# Create empty list
university_name_list     = []
first_name_list          = []
last_name_list           = []
country_list             = []
department_list          = []
center_list              = []
profile_list             = []
email_list               = []
phone_list               = []
specialized_subject_list = []

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/get/academic/data', methods=['GET'])
def get_academic_data():
    global university_name_list, first_name_list, last_name_list, country_list, department_list, center_list, phone_list, profile_list, email_list, specialized_subject_list

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('academic_records_of_universities_faculty.xlsx', engine='xlsxwriter')

    funcs = {
        'georgia_institute_of_technology': [georgia_institute_of_technology],
        'ecole_polytechnique_federale': [ecole_polytechnique_federale],
        'peking_university': [peking_university],
        'university_of_edinburgh': [university_of_edinburgh]
    }

    try:
        for university in app.config['UNIVERSITY_LIST']:
            handlers = funcs[university]
            for handler in handlers:
                handler(university)

                df = pd.DataFrame()
                ## update dataframe
                df['University_Name']           = pd.Series(university_name_list)
                df['Academic_Staff_First_Name'] = pd.Series(first_name_list)
                df['Academic_Staff_Last_Name']  = pd.Series(last_name_list)
                df['Country']                   = pd.Series(country_list)
                df['Department']                = pd.Series(department_list)
                df['Center']                    = pd.Series(center_list)
                df['Profile_Link']              = pd.Series(profile_list)
                df['Contact_number']            = pd.Series(phone_list)
                df['Email_ID']                  = pd.Series(email_list)
                df['Specialized_subject']       = pd.Series(specialized_subject_list)

                # reset list
                university_name_list = []
                first_name_list = []
                last_name_list = []
                country_list = []
                department_list = []
                center_list = []
                profile_list = []
                phone_list = []
                email_list = []
                specialized_subject_list = []

                df = df.drop_duplicates(subset=['Academic_Staff_First_Name', 'Academic_Staff_Last_Name'], keep='last')
                df.reset_index()

                # Convert the dataframe to an XlsxWriter Excel object.
                df.to_excel(writer, sheet_name=university, index=False)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        return "Universities faculty staff's academic record created."
    except Exception as ex:
        print (f'Error in collecting the university data, {ex}')

def populate_column_list(uname=None, fname=None, lname=None, profile=None, email=None, phone=None, dept=None, center=None, university=None, specialization=None):
    university_name_list.append(uname)
    first_name_list.append(fname)
    last_name_list.append(lname)
    profile_list.append(profile)
    email_list.append(email)
    phone_list.append(phone)
    department_list.append(dept)
    center_list.append(center)
    country_list.append(app.config['COUNTRY'][university])
    specialized_subject_list.append(specialization)


def university_of_edinburgh(university):
    university_name = 'University of Edinburgh'
    print(f'Start processing data for:  {university_name}')
    webs = [
            'https://www.ed.ac.uk/medicine-vet-medicine/about/staff-list',
            'https://www.ed.ac.uk/medicine-vet-medicine/edinburgh-medical-school/people',
            'https://www.ed.ac.uk/clinical-sciences/divisionpgdi/clinical-surgical',
            'https://www.ed.ac.uk/dentistry/people/academic-staff',
            'https://www.ed.ac.uk/vet/our-staff',
            'https://www.ed.ac.uk/science-engineering/about/college-office/staff-list',
            'https://www.ed.ac.uk/bayes/about-us/our-team',
            'https://www.ed.ac.uk/biology/people/research',
            'https://www.ed.ac.uk/biology/people/academic/0',
            'http://www.chem.ed.ac.uk/staff',
            'http://www.chem.ed.ac.uk/staff/academic-staff',
            'http://www.chem.ed.ac.uk/staff/postdoctoral',
            'http://www.chem.ed.ac.uk/staff/professional-services-staff',
            'https://www.eng.ed.ac.uk/about/people',
            'https://www.epcc.ed.ac.uk/about/staff',
            'https://www.ed.ac.uk/geosciences/people',
            'https://www.ed.ac.uk/informatics/people/academic',
            'https://www.ed.ac.uk/informatics/people/research',
            'https://www.ed.ac.uk/informatics/people/research-students',
            'https://www.maths.ed.ac.uk/school-of-mathematics/people',
            'https://www.maths.ed.ac.uk/school-of-mathematics/people/academic-staff',
            'https://www.maths.ed.ac.uk/school-of-mathematics/people/postdoc',
            'https://www.maths.ed.ac.uk/school-of-mathematics/people/phd'
            ]
    for web in webs:
        response = requests.get(web)
        data = bs.BeautifulSoup(response.text, 'lxml')

        if web == 'https://www.maths.ed.ac.uk/school-of-mathematics/people':
            print(f"Extracting data from '{web}'")
            homepage = 'https://www.maths.ed.ac.uk'
            tables = data.find_all('table')
            for table in tables:
                trs = table.find_all('tr')
                for tr in trs:
                    a = tr.find('a')
                    if a:
                        profile = a.get('href')
                        profile = f'{homepage}{profile}'
                        name = a.text
                        last_name = name.split(' ')[-1].strip()
                        first_name = ' '.join(name.split(' ')[0:-1]).strip()
                        populate_column_list(uname=university_name, fname=first_name, lname=last_name,
                                             profile=profile, dept='Mathematics', center='People and role holders', university=university)
        if web in ['https://www.maths.ed.ac.uk/school-of-mathematics/people/academic-staff',
                   'https://www.maths.ed.ac.uk/school-of-mathematics/people/postdoc',
                   'https://www.maths.ed.ac.uk/school-of-mathematics/people/phd']:
            print(f"Extracting data from '{web}'")
            homepage = 'https://www.maths.ed.ac.uk'
            if web == 'https://www.maths.ed.ac.uk/school-of-mathematics/people/postdoc':
                center = 'Postdoctoral'
            if web == 'https://www.maths.ed.ac.uk/school-of-mathematics/people/academic-staff':
                center = 'Academic staff'
            if web == 'https://www.maths.ed.ac.uk/school-of-mathematics/people/phd':
                center = 'PhD Students'

            table = data.find('table')
            trs = table.find_all('tr')
            profile, first_name, last_name, email, phone = None,None,None,None,None
            for tr in trs:
                name = tr.find('td', class_='name')
                if name:
                    name = name.find('a')
                    if name:
                        profile = name.get('href')
                        profile = f'{homepage}{profile}'
                        name = name.text
                        name = name.split(',')
                        if len(name) >= 2:
                            first_name = name[-1].strip()
                            last_name = name[0].strip()
                phone = tr.find('td', class_='phone')
                if phone:
                    phone = phone.text
                email = tr.find('td', class_='email')
                if email:
                    email = email.find('a')
                    if email:
                        email = email.text
                populate_column_list(uname=university_name, fname=first_name, lname=last_name, email=email, phone=phone,
                                     profile=profile, dept='Mathematics', center=center, university=university)
        if web in ['https://www.ed.ac.uk/informatics/people/academic', 'https://www.ed.ac.uk/informatics/people/research', 'https://www.ed.ac.uk/informatics/people/research-students']:
            print(f"Extracting data from '{web}'")
            dept = 'Informatics'
            if web == 'https://www.ed.ac.uk/informatics/people/academic':
                center = 'Academic'
            if web == 'https://www.ed.ac.uk/informatics/people/research':
                center = 'Research'
            if web == 'https://www.ed.ac.uk/informatics/people/research-students':
                center = 'Research-student'
            divs = data.find('div', class_='inf-people')
            if not divs:
                divs = data.find('ul', class_='inf-people')
            aa = divs.find_all('a')
            for a in aa:
                profile = a.get('href')
                name = a.text
                last_name = name.split(' ')[-1].strip()
                first_name = ' '.join(name.split(' ')[0:-1]).strip()
                populate_column_list(uname=university_name, fname=first_name, lname=last_name,
                                     profile=profile, dept=dept, center=center, university=university)
        if web == 'https://www.ed.ac.uk/geosciences/people':
            print(f"Extracting data from '{web}'")
            # client_response = Client(web)
            # data = bs.BeautifulSoup(client_response.html, 'lxml')
            homepage = 'https://www.eng.ed.ac.uk'
            # for pn in range(1, 22):
            #     response = requests.get(web).text
            #     render(response)
        if web == 'https://www.epcc.ed.ac.uk/about/staff':
            print(f"Extracting data from '{web}'")
            homepage = 'https://www.epcc.ed.ac.uk'
            fields = data.find_all('span', class_='field-content')
            for field in fields:
                name = field.find('span', class_='name')
                aprofile = field.find_all('a')
                if len(aprofile) == 2 :
                    profile = aprofile[1].get('href')
                    profile = f'{homepage}{profile}'
                if name:
                    name = name.text
                    last_name = name.split(' ')[-1].strip()
                    first_name = ' '.join(name.split(' ')[0:-1]).strip()
                phone = field.find('span', class_='telnumber')
                if phone:
                    phone = phone.text.split(':')[-1].strip()
                email = field.find('span', class_='email')
                if email:
                    email = email.find('a')
                    if email:
                        email = email.text.strip()
                populate_column_list(uname=university_name, fname=first_name, lname=last_name, email=email, phone=phone,
                                     profile=profile, dept='Edinburgh Parallel Computing Centre', university=university)
        if web == 'https://www.eng.ed.ac.uk/about/people':
            print(f"Extracting data from '{web}'")
            homepage = 'https://www.eng.ed.ac.uk'
            for pn in range(0, 28):
                response = requests.get(f'{web}?page={pn}')
                data = bs.BeautifulSoup(response.text, 'lxml')
                table = data.find('table')
                trs = table.find_all('tr')
                del trs[0]
                for tr in trs:
                    tds = tr.find_all('td')
                    name = tds[0]
                    if name:
                        a = name.find('a')
                        if a:
                            profile = a.get('href')
                            profile = f'{homepage}{profile}'
                            name = a.text
                        else:
                            name = name.text
                        last_name = name.split(' ')[-1].strip()
                        first_name = ' '.join(name.split(' ')[0:-1]).strip()
                    phone = tds[2]
                    email = tds[3]
                    if phone:
                        phone = phone.text.strip()
                    if email:
                        email = email.find('a')
                        email = email.text if email else None
                    populate_column_list(uname=university_name, fname=first_name, lname=last_name, email=email, phone=phone,
                                         profile=profile, dept='Engineering Staff', university=university)
        if web in ['http://www.chem.ed.ac.uk/staff/academic-staff', 'http://www.chem.ed.ac.uk/staff/postdoctoral', 'http://www.chem.ed.ac.uk/staff/professional-services-staff']:
            print(f"Extracting data from '{web}'")
            homepage = 'http://www.chem.ed.ac.uk'
            tables = data.find_all('table')
            h2 = data.find_all('h2')
            for h, table in zip(['Academic Staff', 'Honorary Fellows', 'Visiting Professors', 'Honorary Professors', 'Professors Emeritus'], tables):
                trs = table.find_all('tr')
                del trs[0]
                for tr in trs:
                    tds = tr.find_all('td')
                    name = tds[0]
                    if name:
                        a = name.find('a')
                        if a:
                            profile = a.get('href')
                            profile = f'{homepage}{profile}'
                            name = a.text
                        else:
                            name = name.text
                        last_name = name.split(' ')[-1].strip()
                        first_name = ' '.join(name.split(' ')[0:-1]).strip()
                    if web == 'http://www.chem.ed.ac.uk/staff/professional-services-staff':
                        phone = tds[3]
                        email = tds[2]
                        h = 'Professional Services Staff'
                    else:
                        phone = tds[2]
                        email = tds[1]
                    if phone:
                        phone = phone.text.strip()
                    if email:
                        email = email.find('a')
                        email = email.text if email else None
                    if web == 'http://www.chem.ed.ac.uk/staff/postdoctoral':
                        h = 'Postdoctoral Researchers'
                    populate_column_list(uname=university_name, fname=first_name, lname=last_name, email=email, phone=phone,
                                         profile=profile, dept='Chemistry Staff', university=university, center=h)
        if web == 'http://www.chem.ed.ac.uk/staff':
            print(f"Extracting data from '{web}'")
            tables = data.find_all('table')
            h3 = data.find_all('h3')
            for h, table in zip(h3, tables):
                trs = table.find_all('tr')
                del trs[0]
                for tr in trs:
                    tds = tr.find_all('td')
                    #print(tds)
                    name = tds[1]
                    if name:
                        name = name.text
                        last_name = name.split(' ')[-1].strip()
                        first_name = ' '.join(name.split(' ')[0:-1]).strip()
                    phone = tds[2]
                    if phone:
                        phone = phone.text.strip()
                    email = tds[3]
                    if email:
                        email = email.find('a').text
                    populate_column_list(uname=university_name, fname=first_name, lname=last_name, email=email,
                                         dept='Chemistry Staff', university=university, center=h)
        if web in ['https://www.ed.ac.uk/biology/people/research', 'https://www.ed.ac.uk/biology/people/academic/0']:
            print(f"Extracting data from '{web}'")
            if web =='https://www.ed.ac.uk/biology/people/research':
                center = 'Research Staff'
            if web == 'https://www.ed.ac.uk/biology/people/academic/0':
                center = 'Academic Staff'
            table = data.find('table', id='proxy_academics')
            trs = table.find_all('tr')
            del trs[0]
            first_name, last_name,profile, email = None,None,None,None
            for tr in trs:
                tds = tr.find_all('td')
                name = tds[0]
                if name:
                    a = name.find('a')
                    if a:
                        profile = a.get('href')
                        name = a.text
                    else:
                        name = name.text
                    last_name, first_name = name.split(',')
                    if first_name:
                        first_name = first_name.strip()
                    if last_name:
                        last_name = last_name.strip()
                if len(tds) > 5:
                    email = tds[3]
                else:
                    email = tds[2]

                if email:
                    email = email.find('a')
                    if email:
                        email = email.text.strip()
                populate_column_list(uname=university_name, fname=first_name, lname=last_name, profile=profile, email=email,
                                     dept='Biological Sciences', university=university, center=center)
        if web in ['https://www.ed.ac.uk/science-engineering/about/college-office/staff-list',
                   'https://www.ed.ac.uk/bayes/about-us/our-team']:
            print(f"Extracting data from '{web}'")
            if web == 'https://www.ed.ac.uk/science-engineering/about/college-office/staff-list':
                dept = 'Bayes Centre'
            if web == 'https://www.ed.ac.uk/bayes/about-us/our-team':
                dept = 'Science & Engineering'
            homepage = 'https://www.ed.ac.uk'
            tables = data.find_all('table')
            del tables[0]
            for table in tables:
                trs = table.find_all('tr')
                del trs[0]
                for tr in trs:
                    tds = tr.find_all('td')
                    if len(tds) >= 3:
                        name = tds[0].find('a')
                        if name:
                            profile = name.get('href')
                            if 'http' not in profile:
                                profile = f'{homepage}{profile}'
                            name = name.text
                            last_name = name.split(' ')[-1].strip()
                            first_name = ' '.join(name.split(' ')[0:-1]).strip()
                        else:
                            if name:
                                name = name.text
                                last_name = name.split(' ')[-1].strip()
                                first_name = ' '.join(name.split(' ')[0:-1]).strip()
                        center = tds[1]
                        if center:
                            center = center.text.strip()
                        email = tds[2].find('a')
                        if email:
                            email = email.text.strip()
                        if len(tds) > 3:
                            phone = tds[3]
                            if phone:
                                phone = phone.text.strip()
                        populate_column_list(uname=university_name, fname=first_name, profile=profile, lname=last_name,
                                             email=email, phone=phone, dept=dept, university=university, center=center)
        if web == 'https://www.ed.ac.uk/vet/our-staff':
            print(f"Extracting data from '{web}'")
            homepage = 'https://www.ed.ac.uk'
            table = data.find('table')
            trs = table.find_all('tr')
            del trs[0]
            for tr in trs:
                tds = tr.find_all('td')
                name = tds[0].find('a')
                if name:
                    profile = name.get('href')
                    profile = f'{homepage}{profile}'
                    name = name.text
                    last_name = name.split(' ')[-1].strip()
                    first_name = ' '.join(name.split(' ')[0:-1]).strip()
                center = tds[1].text.strip()
                populate_column_list(uname=university_name, fname=first_name, profile=profile, lname=last_name,
                                     dept='Veterinary Studies', university=university, center=center)
        if web == 'https://www.ed.ac.uk/dentistry/people/academic-staff':
            print(f"Extracting data from '{web}'")
            homepage = 'https://www.ed.ac.uk'
            rows = data.find_all('section', id='block-system-main')
            links = rows[0].find_all('a')
            for link in links:
                profile = link.get('href')
                profile = f'{homepage}{profile}'
                r = requests.get(profile)
                data = bs.BeautifulSoup(r.text, 'lxml')
                header = data.find('header')
                first_name = header.find('span', itemprop='givenName').text
                last_name = header.find('span', itemprop='familyName').text
                ul = data.find('ul', class_='list-contact')
                if ul:
                    lis = ul.find_all('li')
                    for li in lis:
                        phone = li.find('a', itemprop='telephone')
                        if phone:
                            phone = phone.text
                        email = li.find('a', itemprop='email')
                        if email:
                            email = email.text
                    populate_column_list(uname=university_name, fname=first_name, profile=profile, lname=last_name,
                                         email=email, phone=phone, dept='Dental', center='Academic staff', university=university)
        if web == 'https://www.ed.ac.uk/clinical-sciences/divisionpgdi/clinical-surgical':
            print(f"Extracting data from '{web}'")
            section = data.find('div', itemprop='mainContentOfPage')
            divs = section.find_all('div')
            for div in divs:
                pp = div.find_all('p')
                emm = pp[0].find('a').get('href').split(':')[-1]
                populate_column_list(uname=university_name, fname='Tim', lname='Walsh', phone='+44 (0)131 242 6395',
                                     email=emm, university=university, dept='Clinical Sciences')
                del pp[0:2]
                ll = [pp[i:i + 3] for i in range(0, len(pp), 3)]
                for l in ll:
                    p = l[0].text
                    if p:
                        name, phone = p.split(',')
                    email = l[1].find('a').get('href')
                    if email:
                        email = email.split(':')[-1]
                    name = name.split('Professor')[-1]
                    if name:
                        last_name = name.split(' ')[-1].strip()
                        first_name = ' '.join(name.split(' ')[0:-1]).strip()
                    if phone:
                        phone = phone.split(':')[-1].strip()
                    populate_column_list(uname=university_name, fname=first_name, lname=last_name, phone=phone,
                                         email=email, university=university, dept='Clinical Sciences')
            populate_column_list(uname=university_name, fname='AHRW', lname='Simpson', phone='+44 (0)131 242 6644',
                                 email='hamish.simpson@ed.ac.uk', university=university, dept='Clinical Sciences')
            populate_column_list(uname=university_name, fname='A', lname='MacLullich', phone='+44 (0)131 242 6481',
                                 email='a.maclullich@ed.ac.uk', university=university, dept='Clinical Sciences')
        if web == 'https://www.ed.ac.uk/medicine-vet-medicine/about/staff-list':
            print(f"Extracting data from '{web}'")
            tables = data.find_all('table', class_='table')
            for table in tables:
                dept = table.find('caption').text
                trs = table.find_all('tr')
                del trs[0]
                for tr in trs:
                    td = tr.find_all('td')
                    name = td[0].text
                    last_name = name.split(' ')[-1].strip()
                    first_name = ' '.join(name.split(' ')[0:-1]).strip()
                    phone = td[2].text
                    if phone in ['on secondment', 'on maternity leave']:
                        phone = None
                    email = td[3].find('a')
                    if email:
                        email = email.get('href')

                    populate_column_list(uname=university_name, fname=first_name, lname=last_name, phone=phone,
                                         email=email, university=university, dept='Medicine & Veterinary Medicine',
                                         center='Office Staff')


def peking_university(university):
    university_name = 'Peking University'
    print(f'Start processing data for:  {university_name}')
    webs = ['http://scbb.pkusz.edu.cn/en/faculty/ddc/', 'http://scbb.pkusz.edu.cn/en/faculty/nmm/',
            'http://scbb.pkusz.edu.cn/en/faculty/SOMC/', 'http://scbb.pkusz.edu.cn/en/faculty/ccsb/']
    for web in webs:
        print(f"Extracting data from '{web}'")
        response = requests.get(web)
        data = bs.BeautifulSoup(response.text, 'lxml')
        lis = data.find_all('li', class_='teacher-list')
        first_name, last_name, name, profile, email, phone = None, None, None, None, None, None
        for li in lis:
            liss = li.find_all('li')
            name = liss[0].find('a')
            if name:
                profile = name.get('href')
                name = name.text
                last_name = name.split(' ')[-1].strip()
                first_name = ' '.join(name.split(' ')[0:-1]).strip()
            center = liss[1].text
            phone = liss[2].text.split(':')[-1].strip()
            email = liss[3].text.split(':')[-1].strip()
            if 'SOMC' in web:
                department_list.append('Synthetic Chemistry')
            if 'ddc' in web:
                department_list.append('Translational Biology')
            if 'nmm' in web:
                department_list.append('Chemical Biology')
            if 'ccsb' in web:
                department_list.append('Computational Chemistry')
            populate_column_list(uname=university_name, fname=first_name, lname=last_name, phone=phone,
                                 email=email, profile=profile, university=university)


def ecole_polytechnique_federale(university):
    university_name = 'Ecole Polytechnique Federale de Lausanne'
    print(f'Start processing data for:  {university_name}')
    webs = [
            'https://www.epfl.ch/schools/sb/research/isic/faculty-members/',
            'https://www.epfl.ch/schools/sv/school-of-life-sciences/professors/',
            'https://sti.epfl.ch/research/faculty-members/',
            'https://www.epfl.ch/research/faculty-members/'
    ]
    for web in webs:
        response = requests.get(web)
        data = bs.BeautifulSoup(response.text, 'lxml')
        if web == 'https://www.epfl.ch/schools/sb/research/isic/faculty-members/':
            print(f"Extracting data from '{web}'")
            divs = data.find_all('div', class_='container-full')
            for div in divs:
                divs = div.find_all('div', class_='card-body')
                first_name, last_name, name, center, profile = None, None, None, None, None
                for div in divs:
                    name = div.find('a', class_='h3')
                    center = div.find('a', target='_blank')
                    if name:
                        profile = name.get('href')
                        name = name.text.split(',')[0]
                        last_name = name.split(' ')[0]
                        first_name = ' '.join(name.split(' ')[1:]).strip()
                    if center:
                        center = center.text

                    populate_column_list(uname=university_name, fname=first_name, lname=last_name, profile=profile,
                                         dept='Chemical Sciences and Engineering', center='Faculty Members', university=university)

        if web == 'https://www.epfl.ch/schools/sv/school-of-life-sciences/professors/':
            print(f"Extracting data from '{web}'")
            divs = data.find_all('div', class_='contact-list-row')
            name, first_name, last_name, email, phone = None, None, None, None, None
            for div in divs:
                name = div.find('a', class_='contact-list-item')
                email = div.find('a', itemprop='email')
                phone = div.find('a', itemprop='telephone')
                if name:
                    profile = name.get('href')
                    name = name.text
                    first_name = ' '.join(name.split(' ')[0:-1]).strip()
                    last_name = name.split(' ')[-1]
                if email:
                    email = email.text
                if phone:
                    phone = phone.text

                populate_column_list(uname=university_name, fname=first_name, lname=last_name, phone=phone,
                                     email=email, profile=profile, dept='Life Sciences',
                                     center='Professors', university=university)
        if web == 'https://sti.epfl.ch/research/faculty-members/':
            print(f"Extracting data from '{web}'")
            response = requests.get(web).text
            data = bs.BeautifulSoup(render(response), 'lxml')
            divs = data.find('div', class_='row', id='faculty-gallery')
            div  = divs.find_all('div', class_='faculty-titre-card')
            first_name, last_name, name, profile, center = None, None, None, None, None
            for d in div:
                dd = d.find('div', class_='faculty-titre-id')
                name  = dd.find('a')
                if name:
                    profile = name.get('href')
                    name = name.text
                    last_name  = ' '.join(name.split(' ')[0:-1]).strip()
                    first_name = name.split(' ')[-1]
                    populate_column_list(uname=university_name, fname=first_name, lname=last_name,
                                     profile=profile, dept='Engineering',center='Faculty Members', university=university)
        if web == 'https://www.epfl.ch/research/faculty-members/':
            print(f"Extracting data from '{web}'")
            divs = data.findAll('div', class_='contact-list-row')
            for div in divs:
                name = div.find_all('a', itemprop='name')
                first_name, last_name, profile, email, phone, address, center = None, None, None, None, None, None, None
                if name:
                    profile = name[0].get('href')
                    name = name[0].text
                    first_name = ' '.join(name.split(' ')[0:-1]).strip()
                    last_name = name.split(' ')[-1]
                email = div.find_all('a', itemprop='email')
                phone = div.find_all('a', href='tel:')
                if phone:
                    phone = phone[0].text.strip()
                if email:
                    email = email[0].text.strip()
                populate_column_list(uname=university_name, fname=first_name, lname=last_name,email=email, phone=phone,
                                     profile=profile, dept='Research', center='Faculty Members', university=university)


def georgia_institute_of_technology(university):
    university_name = 'Georgia Institute of Technology'
    print(f'Start processing data for:  {university_name}')
    webs = ['https://psychology.gatech.edu/people',
            'https://physics.gatech.edu/people/graduate-students',
            'https://physics.gatech.edu/people/postdoctoral-researchers',
            'https://physics.gatech.edu/people/research-scientists',
            'https://physics.gatech.edu/people/professors-of-practice',
            'https://physics.gatech.edu/people/adjunct-faculty',
            'https://physics.gatech.edu/people/professors',
            'https://www.chemistry.gatech.edu/directory/all',
            'https://biosciences.gatech.edu/people',
            'https://eas.gatech.edu/people']
    for web in webs:
        response = requests.get(web)
        data = bs.BeautifulSoup(response.text, 'lxml')
        if web == 'https://psychology.gatech.edu/people':
            print(f"Extracting data from '{web}'")
            homepage = 'https://psychology.gatech.edu'
            table = data.find_all('table')
            trs = table[0].find_all('tr')
            del trs[0]
            for tr in trs:
                tds = tr.find_all('td')
                name = tds[0].find_all('a')
                profile, first_name, last_name, email, phone = None, None, None, None, None
                if name:
                    profile = name[0].get('href')
                    name = name[0].text.strip()
                    name = name.split(' ')
                    if len(name) > 2:
                        first_name = f'{name[0]} {name[1]}'
                        last_name = name[2]
                    else:
                        first_name = name[0]
                        last_name = name[1]

                    profile = f'{homepage}{profile}'
                email = tds[1].text
                if email:
                    email = email.strip()
                phone = tds[2].text
                if phone:
                    phone = phone.strip()
                populate_column_list(uname=university_name, fname=first_name, lname=last_name, email=email, phone=phone,
                                     profile=profile, dept='Psychology', university=university)
        if 'https://www.chemistry.gatech.edu/directory/all' == web:
            print(f"Extracting data from '{web}'")
            homepage = 'https://www.chemistry.gatech.edu/'
            table = data.find_all('table')
            trs = table[0].find_all('tr')
            del trs[0]
            for tr in trs:
                tds = tr.find_all('td')
                last_name = tds[0].text.strip()
                first_name = tds[1].text.strip()
                profile = tds[1].find_all('a')[0].get('href')
                profile = f'{homepage}{profile}'
                email = tds[4].find_all('a')
                if email:
                    email = email[0].get('href').split(':')[-1]
                phone = tds[4].text.split('\n')
                if phone:
                    phone = phone[-1]
                populate_column_list(uname=university_name, fname=first_name, lname=last_name, email=email, phone=phone,
                                     profile=profile, dept='Chemistry and Biochemistry', university=university)
        if 'https://biosciences.gatech.edu/people' == web:
            print(f"Extracting data from '{web}'")
            homepage = 'https://biosciences.gatech.edu/'
            lis = data.find_all('li')
            for li in lis:
                divs = li.find_all('div', class_='biosci-details')

                if divs:
                    a = divs[0].find_all('a')
                    if a:
                        name = a[0].text
                        first_name = ' '.join(name.split(' ')[0:-1]).strip()
                        last_name = name.split(' ')[-1]
                        profile = a[0].get('href')
                        profile = f'{homepage}{profile}'
                        populate_column_list(uname=university_name, fname=first_name, lname=last_name,
                                             profile=profile, dept='Biological Sciences', university=university)
        if 'https://eas.gatech.edu/people' == web:
            print(f"Extracting data from '{web}'")
            homepage = 'https://eas.gatech.edu'
            lis = data.find_all('li')
            for li in lis:
                divs = li.find_all('div', class_='eas-details')
                if divs:
                    a = divs[0].find_all('a')
                    if a:
                        name = a[0].text
                        if ',' in name:
                            last_name, first_name = name.split(',')
                        elif ' ' in name:
                            name = name.split(' ')
                            if len(name) > 2:
                                first_name = f'{name[0]} {name[1]}'
                                last_name = name[2]
                            else:
                                first_name = name[0]
                                last_name = name[1]
                        else:
                            first_name = name.strip()
                            last_name = None

                        profile = a[0].get('href')
                        profile = f'{homepage}{profile}'
                        populate_column_list(uname=university_name, fname=first_name, lname=last_name,
                                             profile=profile, dept='Earth and Atmospheric Sciences', university=university)
        if web in ['https://physics.gatech.edu/people/graduate-students', 'https://physics.gatech.edu/people/postdoctoral-researchers', 'https://physics.gatech.edu/people/research-scientists', 'https://physics.gatech.edu/people/professors-of-practice', 'https://physics.gatech.edu/people/professors', 'https://physics.gatech.edu/people/adjunct-faculty']:
            print(f"Extracting data from '{web}'")
            homepage = 'https://physics.gatech.edu'
            center = None
            if web == 'https://physics.gatech.edu/people/professors-of-practice':
                center = 'Professors of Practice'
            if web == 'https://physics.gatech.edu/people/professors':
                center = 'Tenure-Track and Tenured Professors'
            if web == 'https://physics.gatech.edu/people/adjunct-faculty':
                center = 'Adjunct Faculty'
            if web == 'https://physics.gatech.edu/people/research-scientists':
                center = 'Research Scientists'
            if web == 'https://physics.gatech.edu/people/postdoctoral-researchers':
                center = 'Postdoctoral Researchers'
            if web == 'https://physics.gatech.edu/people/graduate-students':
                center = 'Graduate Students'
            divs = data.find_all('div', class_='field-content')
            for div in divs:
                atag = div.find_all('a')
                if atag:
                    name = atag[0].text
                    name = name.split(' ')
                    if len(name) > 2:
                        first_name = f'{name[0]} {name[1]}'
                        last_name = name[2]
                    else:
                        first_name= name[0]
                        last_name = name[1]
                    profile = atag[0].get('href')
                    profile = f'{homepage}{profile}'
                    populate_column_list(uname=university_name, fname=first_name, lname=last_name,
                                         profile=profile, dept='Physics', center=center, university=university)


if __name__ == '__main__':
   app.run(host='localhost', debug=True)