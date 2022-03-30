import json
import logging
import re
import requests


class ProblemParser:
    url = 'https://leetcode.com/graphql'

    headers = {
        'referer': 'https://leetcode.com/uwi/',
        'cookie': "csrftoken=072x9rHWNg1kkNXwiJ3BH2RNd8sKxZ5jbByD8upwAX2sq9sLHxyLko43D4yq4UE7; __cfduid=d200def86257d1bc29ba00c6c8b3ad20c1610345109; csrftoken=0HAcMpAuL6Fte9Af18y98z2T3gvV84PHTy673AOkl3q8mGebGIOHHgLwaUzBo11x",
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
    }

    @staticmethod
    def _get_data(problem_id: str):
        return {
            'operationName': 'questionData',
            'variables': {
                'titleSlug': problem_id 
            },
            'query': 'query questionData($titleSlug: String!) {\n question(titleSlug: $titleSlug) {\n questionId\n questionFrontendId\n boundTopicId\n title\n titleSlug\n content\n translatedTitle\n translatedContent\n isPaidOnly\n difficulty\n likes\n dislikes\n isLiked\n similarQuestions\n exampleTestcases\n contributors {\n username\n profileUrl\n avatarUrl\n __typename\n }\n topicTags {\n name\n slug\n translatedName\n __typename\n }\n companyTagStats\n codeSnippets {\n lang\n langSlug\n code\n __typename\n }\n stats\n hints\n solution {\n id\n canSeeDetail\n paidOnly\n hasVideoSolution\n paidOnlyVideo\n __typename\n }\n status\n sampleTestCase\n metaData\n judgerAvailable\n judgeType\n mysqlSchemas\n enableRunCode\n enableTestMode\n enableDebugger\n envInfo\n libraryUrl\n adminUrl\n challengeQuestion {\n id\n date\n incompleteChallengeCount\n streakCount\n type\n __typename\n }\n __typename\n }\n}\n'
        }
    
    @staticmethod
    def query(problem_id: str):
        ret = None
        try:
            response = None
            with requests.Session() as s:
                s.headers = ProblemParser.headers
                r = s.post(
                    ProblemParser.url, 
                    data=json.dumps(ProblemParser._get_data(problem_id))
                )
                response = json.loads(r.text)['data']['question']
            ret = {
                'questionId': response['questionId'],
                'title': response['title'],
                'difficulty': response['difficulty'],
                'url': f'https://leetcode.com/problems/{problem_id}',
                'title': response['title'],
                'isPaidOnly': response['isPaidOnly'],
                'likes': response['likes'],
                'dislikes': response['dislikes'],
                'content': re.sub('<[^<]+?>', '', response['content'])
                    .replace('\n', ' ').replace('&nbsp;', ' ')
            }
        except Exception as e:
            logging.error(e)
        return ret

print (ProblemParser.query('two-sum'))

