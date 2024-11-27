from django.shortcuts import render
import requests, os, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from golf.models import Reservation

# Create your views here.

# def index(request):
#     return render(request, 'golf/index.html')


def scraping(request):
    Reservation.objects.all().delete()
    if not Reservation.objects.all():
        login_url = 'https://olympus.aptner.com/OLYMPUS//login.do?admin=Y'
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('window-size=1920x1080')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(login_url)

        username = 'urvinehs'
        password = '1234'


        login_url = 'https://olympus.aptner.com/OLYMPUS//login.do?admin=Y'
        username_input = driver.find_element(By.XPATH, '//*[@id="ip_id"]')
        password_input = driver.find_element(By.XPATH, '//*[@id="ip_pw"]')
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = driver.find_element(By.XPATH, '//*[@id="btn_login"]')
        login_button.click()
        time.sleep(1)

        # 캘린더 프레임으로 이동
        frame_element = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/iframe')
        time.sleep(1)
        driver.switch_to.frame(frame_element)
        time.sleep(1)
        # # 오늘 날짜 선택
        formatted_current_day = datetime.now().strftime('%Y-%m-%d')

        date_tap = driver.find_element(
            By.XPATH,
            f'//td[contains(@class, "fc-day-top") and contains(@data-date, "{formatted_current_day}")]')
        date_tap.click()
        time.sleep(1)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        name = soup.select('#main_grid tbody td:nth-child(n+2):nth-child(-n+5)')
        time.sleep(1)
        driver.close()
        # 데이터 model로 저장
        previous_home = ''
        temp_count = 0
        reservation = Reservation()
        for content in name:     
            if temp_count % 4 == 0:
                reservation.room = content.get_text()
            elif temp_count % 4 == 1:
                reservation.time = content.get_text()
            elif temp_count % 4 == 2:
                reservation.name = content.get_text()
            elif temp_count % 4 == 3:
                reservation.home = content.get_text()
                if (
                    reservation.room != '스크린골프(2단지)' and
                    reservation.room != '스크린골프6' and
                    reservation.home != previous_home
                ):
                    reservation.save()
                else: 
                    existing_reservation = Reservation.objects.filter(
                        room=reservation.room,
                        name=reservation.name,
                        home=reservation.home
                    ).last()
                    if existing_reservation:
                        existing_reservation.time = existing_reservation.time[:5] + " ~ " + reservation.time[8:]
                        existing_reservation.save()                
                previous_home = reservation.home
                reservation = Reservation()
            temp_count += 1
        
    context = dict()
    reservations_1 = Reservation.objects.filter(room='스크린골프1')
    reservations_2 = Reservation.objects.filter(room='스크린골프2')
    reservations_3 = Reservation.objects.filter(room='스크린골프3')
    reservations_4 = Reservation.objects.filter(room='스크린골프4')
    reservations_5 = Reservation.objects.filter(room='스크린골프5')
    now_hour = str(datetime.now().time().strftime("%H"))
    now_time = datetime.now().time().strftime("%H:%M")
    context['now_time'] = now_time
    # context['reservations_1'] = reservations_1
    # context['reservations_2'] = reservations_2
    # context['reservations_3'] = reservations_3
    # context['reservations_4'] = reservations_4
    # context['reservations_5'] = reservations_5
    if reservations_1:
        for content in reservations_1:
            if content.time[:2] <= now_hour and content.time[8:10] > now_hour:
                current_reservation_1 = content
                break
            else:
                current_reservation_1 = ''
    else:
        current_reservation_1 = ''
    if reservations_2:
        for content in reservations_2:
            if content.time[:2] <= now_hour and content.time[8:10] > now_hour:
                current_reservation_2 = content
                break
            else:
                current_reservation_2 = ''
    else:
        current_reservation_2 = ''    
    if reservations_3:
        for content in reservations_3:
            if content.time[:2] <= now_hour and content.time[8:10] > now_hour:
                current_reservation_3 = content
                break
            else:
                current_reservation_3 = ''
    else:
        current_reservation_3 = ''
    if reservations_4:
        for content in reservations_4:
            if content.time[:2] <= now_hour and content.time[8:10] > now_hour:
                current_reservation_4 = content
                break
            else:
                current_reservation_4 = ''
    else:
        current_reservation_4 = ''
    if reservations_5:        
        for content in reservations_5:
            if content.time[:2] <= now_hour and content.time[8:10] > now_hour:
                current_reservation_5 = content
                break
            else:
                current_reservation_5 = ''
    else:
        current_reservation_5 = ''
    
    
    if current_reservation_1:
        context['current_reservation_1'] = current_reservation_1

    if current_reservation_2:
        context['current_reservation_2'] = current_reservation_2
        
    if current_reservation_3:
        context['current_reservation_3'] = current_reservation_3
        
    if current_reservation_4:
        context['current_reservation_4'] = current_reservation_4
        
    if current_reservation_5:
        context['current_reservation_5'] = current_reservation_5
        
        
    next_reservation_1 = Reservation.objects.filter(room='스크린골프1', time__gt=now_time).first()
    if next_reservation_1:
        context['next_reservation_1'] = next_reservation_1
        
    next_reservation_2 = Reservation.objects.filter(room='스크린골프2', time__gt=now_time).first()    
    if next_reservation_2:
        context['next_reservation_2'] = next_reservation_2
    
    next_reservation_3 = Reservation.objects.filter(room='스크린골프3', time__gt=now_time).first()    
    if next_reservation_3:
        context['next_reservation_3'] = next_reservation_3
    
    next_reservation_4 = Reservation.objects.filter(room='스크린골프4', time__gt=now_time).first()    
    if next_reservation_4:
        context['next_reservation_4'] = next_reservation_4
        
    next_reservation_5 = Reservation.objects.filter(room='스크린골프5', time__gt=now_time).first()
    if next_reservation_5:
        context['next_reservation_5'] = next_reservation_5
        
    return render(request, 'golf/index.html', context=context)
