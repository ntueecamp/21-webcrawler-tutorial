import requests
import json
import codecs

BASE_URL = 'https://www.instagram.com/'
LOGIN_URL = BASE_URL + 'accounts/login/ajax/'


USERNAME='<your email address or username>'
PASSWORD = '<your encoded password>'

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'

ig_userID = 0

session = requests.Session()
session.headers = {'user-agent' : USER_AGENT}
session.headers.update({'Referer' : BASE_URL,'X-IG-Connection-Type': 'WIFI'})

req = session.get(BASE_URL)
# we need to update our request header 'x-csrftoken' to the csrftoken server generated for us to prepare for our next request
session.headers.update({'x-csrftoken':req.cookies['csrftoken']})

login_data = {'username' : USERNAME, 'enc_password' : PASSWORD}


req_login = session.post(LOGIN_URL,data=login_data,allow_redirects = True)
print(req_login.text)

ig_userID =json.loads(req_login.text)['userId']
print("UserID = " + ig_userID)

session.headers.update({'x-csrftoken':req_login.cookies['csrftoken']})
req_feed = session.get(BASE_URL)
session.headers.update({'x-csrftoken':req_feed.cookies['csrftoken']})

print(req_feed.text)

raw_content = req_feed.text

CONFIG_KEYWORD = "window._sharedData = "
config_start_pos = raw_content.find(CONFIG_KEYWORD) + len(CONFIG_KEYWORD)
config_end_pos = raw_content.find("</script>",config_start_pos) - 1

FEED_KEYWORD = "window.__additionalDataLoaded('feed',"
feed_start_pos = raw_content.find(FEED_KEYWORD,config_end_pos) + len(FEED_KEYWORD)
feed_end_pos = raw_content.find("</script>",feed_start_pos) - 2

data_config = json.loads(raw_content[config_start_pos:config_end_pos])
data_feed = json.loads(raw_content[feed_start_pos:feed_end_pos])


fp = codecs.open('data_config.json', 'w', 'utf-8')
fp.write(json.dumps(data_config,ensure_ascii=False))
fp.close()

fp = codecs.open('data_feed.json', 'w', 'utf-8')
fp.write(json.dumps(data_feed,ensure_ascii=False))
fp.close()


# like
POST_ID = '<postID>'
LIKE_URL = "https://www.instagram.com/web/likes/{}/like/".format(POST_ID)

req_like = session.post(LIKE_URL,allow_redirects = True)
session.headers.update({'x-csrftoken':req_like.cookies['csrftoken']})
print(req_like.text)

# unlike
POST_ID = '<postID>'
UNLIKE_URL = "https://www.instagram.com/web/likes/{}/unlike/".format(POST_ID)
req_unlike = session.post(UNLIKE_URL,allow_redirects = True)
session.headers.update({'x-csrftoken':req_unlike.cookies['csrftoken']})
print(req_unlike.text)
