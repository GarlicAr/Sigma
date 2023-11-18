# import requests
#
# from src.config.config import reddit_header_for_videos
# from moviepy.editor import VideoFileClip, AudioFileClip
#
#
# def get_url(url):
#     if not url.startswith('http'):
#         url = 'https://' + url
#     return url + '.json'
#
# try:
#     def reddit_video(url_input):
#         url = get_url(url_input)
#
#         # Update your headers here if needed
#         headers = reddit_header_for_videos
#         r = requests.get(url, headers=headers)
#         r.raise_for_status()
#
#         data = r.json()
#
#         video_url = data[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
#         video_response = requests.get(video_url)
#
#         with open('temp_video.mp4', 'wb') as vfile:
#             vfile.write(video_response.content)
#
#         return 'temp_video.mp4'
#
#
# except requests.exceptions.RequestException as e:
#     print(f"Error: {e}")


from selenium import webdriver
import time
import requests

def download_video(url_input):
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(executable_path='[PATH_TO_CHROMEDRIVER]')
    driver.get("https://tuberipper.com/16/site/reddit")

    # Input the Reddit video link
    input_element = driver.find_element_by_id("videoUrl")
    input_element.send_keys(url_input)

    # Submit the form (this might need to be adjusted based on the website's structure)
    submit_button = driver.find_element_by_id("[SUBMIT_BUTTON_ID]")
    submit_button.click()

    # Wait for the download link to be generated
    time.sleep(10)  # Adjust the waiting time as needed

    # Retrieve the download link (the method of retrieval will depend on the website's structure)
    download_link = driver.find_element_by_id("[DOWNLOAD_LINK_ELEMENT_ID]").get_attribute('href')

    driver.quit()

    # Download the video using the retrieved link
    video_response = requests.get(download_link)
    with open('downloaded_video.mp4', 'wb') as vfile:
        vfile.write(video_response.content)

    return 'downloaded_video.mp4'
