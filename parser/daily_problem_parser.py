import json
import logging
import re
import requests


class DailyProblemParser:
    url = 'https://leetcode.com/graphql'

    headers = {
        'referer': 'https://leetcode.com/problemset/all/',
        'cookie': 'csrftoken=FJx6jPqTahmp7Zvj4D4bjtCE5wtNxmMcnWtDPJ9dDgz2cPFEGJzvukeLoSjMyHmv; 87b5a3c3f1a55520_gr_session_id=23936fcd-7973-422f-9839-2e9899b6b31c; 87b5a3c3f1a55520_gr_session_id_23936fcd-7973-422f-9839-2e9899b6b31c=true; _ga=GA1.2.786612825.1636614285; _gid=GA1.2.201467459.1636614285; gr_user_id=a99c7dea-6a39-489f-8fd9-f3cf3039b10d; NEW_PROBLEMLIST_PAGE=1; _gat=1',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
        'x-csrftoken': 'FJx6jPqTahmp7Zvj4D4bjtCE5wtNxmMcnWtDPJ9dDgz2cPFEGJzvukeLoSjMyHmv',
    }

    @staticmethod
    def _get_data():
        return {
            'operationName': 'questionOfToday',
            'variables': {
            },
            'query': 'query questionOfToday {activeDailyCodingChallengeQuestion {    date    userStatus    link    question {      acRate      difficulty      freqBar      frontendQuestionId: questionFrontendId      isFavor      paidOnly: isPaidOnly      status      title      titleSlug likes dislikes content      hasVideoSolution      hasSolution      topicTags {        name        id        slug      }    }  }}'
        }
    
    @staticmethod
    def query():
        ret = None
        try:
            response = None
            with requests.Session() as s:
                s.headers = DailyProblemParser.headers
                r = s.post(
                    DailyProblemParser.url, 
                    data=json.dumps(DailyProblemParser._get_data())
                )
                print (r.text)
                response = json.loads(r.text)['data']['activeDailyCodingChallengeQuestion']['question']
            ret = {
                'questionId': response['frontendQuestionId'],
                'title': response['title'],
                'difficulty': response['difficulty'],
                'url': f'https://leetcode.com/problems/{response["titleSlug"]}',
                'title': response['title'],
                'isPaidOnly': response['paidOnly'],
                'likes': response['likes'],
                'dislikes': response['dislikes'],
                'content': re.sub('<[^<]+?>', '', response['content'])
                    .replace('\n', ' ').replace('&nbsp;', ' ')
            }
        except Exception as e:
            logging.error(e)
        return ret

