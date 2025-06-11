# References:
# https://www.selenium.dev/documentation/webdriver/browsers/chrome/
# https://stackoverflow.com/questions/74578175/getting-video-links-from-youtube-channel-in-python-selenium
# https://stackoverflow.com/questions/73560123/how-to-extract-the-comments-count-correctly
# https://stackoverflow.com/questions/74028427/chromedriver-executable-needs-to-be-in-path/74029548#74029548
# https://stackoverflow.com/questions/49323099/webdriverexception-message-service-chromedriver-unexpectedly-exited-status-co
# https://askubuntu.com/questions/1514599/how-do-i-install-google-chrome-on-ubuntu-24-04

def fetch_youtube_data(topic, max_results):
    # Import libraries
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    import json
    import os

    AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")
    service = Service(executable_path=AIRFLOW_HOME +
                      "/chromedriver-linux64/chromedriver")

    # Call Chrome Webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-Advertisement")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open YouTube in Google Chrome
        driver.get("https://www.youtube.com/")
        wait = WebDriverWait(driver, 10)

        # Search for the topic query
        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "search_query")))
        search_box.send_keys(topic + Keys.ENTER)
        time.sleep(4)  # Allow page to load

        video_list = []
        counter = 0

        for index in range(1, max_results + 1):
            try:
                driver.execute_script("window.scrollBy(0, arguments[0]);", 600)
                time.sleep(5)
                wait.until(
                    EC.presence_of_element_located(((By.XPATH, f'(//ytd-video-renderer)[{index}]'))))

                video = driver.find_element(
                    By.XPATH, f'(//ytd-video-renderer)[{index}]')

                time.sleep(4)

                video_url = video.find_element(
                    By.XPATH, './/a[@id="thumbnail"]').get_attribute("href")
                video_id = video_url.split("v=")[-1]
                title = video.find_element(By.XPATH, './/h3/a').text

                # Open video page in a new tab
                driver.execute_script("window.open(arguments[0]);", video_url)
                driver.switch_to.window(
                    driver.window_handles[1])  # Switch to new tab
                time.sleep(10)  # Allow video page to load

                try:
                    # Videos with Long Description Box that has to be expanded
                    driver.execute_script(
                        "window.scrollBy(0, arguments[0]);", 500)

                    # Click on '...more' to show full description
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]'))).click()
                    try:
                        views_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="info"]/span[1]'))).text
                        views = views_element.split()[0]
                    except:
                        views = "N/A"

                    try:
                        upload_date_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="info"]/span[3]'))).text
                        if "Premiered on " in upload_date_element:
                            upload_date = upload_date_element.replace(
                                "Premiered on ", "")
                        elif "Premiered " in upload_date_element:
                            upload_date = upload_date_element.replace(
                                "Premiered ", "")
                        else:
                            upload_date = upload_date_element
                    except:
                        upload_date = "N/A"

                    try:
                        likes_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="top-level-buttons-computed"]/segmented-like-dislike-button-view-model/yt-smartimation/div/div/like-button-view-model/toggle-button-view-model/button-view-model/button/div[2]'))).text

                        if likes_element != "Like":
                            # Remove new line character
                            likes = likes_element.replace("\n", "")
                        else:
                            likes = "N/A"
                    except:
                        likes = "N/A"

                    try:
                        description = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="description-inline-expander"]/yt-attributed-string'))).text
                    except:
                        description = "N/A"

                    # Click on 'Show Less' to collapse description box
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[2]'))).click()
                    driver.execute_script(
                        "window.scrollBy(0, arguments[0]);", 500)
                    time.sleep(5)

                    try:
                        comments_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="count"]/yt-formatted-string'))).text
                        comments = comments_element.split()[0]
                    except:
                        comments = "N/A"

                except:
                    # Videos with short Description Box
                    try:
                        views_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="info"]/span[1]'))).text
                        views = views_element.split()[0]
                    except:
                        views = "N/A"

                    try:
                        upload_date_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="info"]/span[3]'))).text
                        if "Premiered on " in upload_date_element:
                            upload_date = upload_date_element.replace(
                                "Premiered on ", "")
                        elif "Premiered " in upload_date_element:
                            upload_date = upload_date_element.replace(
                                "Premiered ", "")
                        else:
                            upload_date = upload_date_element
                    except:
                        upload_date = "N/A"

                    try:
                        likes_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="top-level-buttons-computed"]/segmented-like-dislike-button-view-model/yt-smartimation/div/div/like-button-view-model/toggle-button-view-model/button-view-model/button/div[2]'))).text

                        if likes_element != "Like":
                            # Remove new line character
                            likes = likes_element.replace("\n", "")
                        else:
                            likes = "N/A"
                    except:
                        likes = "N/A"

                    try:
                        description = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="description-inline-expander"]/yt-attributed-string'))).text
                    except:
                        description = "N/A"

                    driver.execute_script(
                        "window.scrollBy(0, arguments[0]);", 500)
                    time.sleep(5)

                    try:
                        comments_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="count"]/yt-formatted-string'))).text
                        comments = comments_element.split()[0]
                    except:
                        comments = "N/A"

                # Store data in dictionary
                video_data = {
                    "Video ID": video_id,
                    "Title": title,
                    "Description": description,
                    "Views": views,
                    "Likes": likes,
                    "Comments": comments,
                    "Upload Date": upload_date,
                    "URL": video_url
                }

                # Exclude YouTube Shorts and duplicates
                if "/watch?v=" in video_url and video_data not in video_list:
                    video_list.append(video_data)
                    counter += 1

                    # counter represents the current number of videos that have been extracted
                    # max_results represents the parameter which we have indicated in youtube_dag.py
                    # counter will always be smaller than max_results as there are duplicates and YouTube shorts
                    print(f"Extracted Video {counter}/{max_results}")

                # Close the video tab and switch back to the search results tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"Error extracting video {counter}: {e}")

        # Write data into JSON file
        topic_stripped = topic.replace(" ", "")
        json_file_path = topic_stripped + ".json"
        print("$AIRFLOW_HOME=", AIRFLOW_HOME)
        with open(json_file_path, "w") as final:
            json.dump(video_list, final)
            print(f"{json_file_path} has been created")

        return video_list

    except Exception as e:
        print("Error:", str(e))
        return None

    finally:
        driver.quit()
