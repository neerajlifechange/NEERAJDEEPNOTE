from splinter import Browser
import asyncio
import nest_asyncio
import getindianname as name

nest_asyncio.apply()

async def start(thread_name, wait_time, meetingcode, passcode):
    user = input(f"Enter name for {thread_name}: ")  # Allow user input for name
    print(f"{thread_name} started! User: {user}")

    # Use Splinter's Browser class with Chrome
    with Browser('chrome', headless=False, incognito=True) as browser:
        # Visit Zoom meeting page
        browser.visit(f'https://zoom.us/wc/join/{meetingcode}')

        try:
            browser.find_by_xpath('//button[@id="onetrust-accept-btn-handler"]').first.click()
        except Exception as e:
            pass

        try:
            # Click the "I Agree" button
            browser.find_by_xpath('//button[@id="wc_agree1"]').first.click()
        except Exception as e:
            pass

        try:
            # Wait for the input fields to become visible
            input_name = browser.find_by_xpath('input[type="text"]').first
            input_password = browser.find_by_xpath('input[type="password"]').first

            # Type the user name and password
            input_name.type(user)
            input_password.type(passcode)

            # Click the "Join" button
            join_button = browser.find_by_xpath('button.preview-join-button').first
            join_button.click()

            # Wait for the "Join Audio by Computer" button to become clickable
            join_audio_button = browser.find_by_xpath('//button[contains(text(), "Join Audio by Computer")]')
            join_audio_button.first.wait_for(lambda b: b['disabled'] == False, timeout=10)
            print(f"{thread_name} mic aayenge.")
        except Exception as e:
            print(f"{thread_name} mic nahe aayenge. ", e)

        # ... (other code)

        print(f"{thread_name} sleep for {wait_time} seconds ...")
        await asyncio.sleep(wait_time)
        print(f"{thread_name} ended!")

def main():
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")

    sec = 90
    wait_time = sec * 60

    loop = asyncio.get_event_loop()
    tasks = []

    for i in range(number):
        thread_name = f'[Thread{i}]'
        task = loop.create_task(start(thread_name, wait_time, meetingcode, passcode))
        tasks.append(task)

    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    except KeyboardInterrupt:
        # Wait for tasks to complete
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
