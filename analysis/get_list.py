import sys, os
from os.path import dirname, abspath
path = dirname(dirname(abspath(__file__)))

sys.path.append(path)

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys
import urlparse
from pprint import pprint
from google.protobuf import text_format

from config import *
from googleplay import GooglePlayAPI
import pprint

import json

class Color:
    Black="\033[0;30m"        # Black
    Red="\033[0;31m"          # Red
    Green="\033[0;32m"        # Green
    Yellow="\033[0;33m"       # Yellow
    Blue="\033[0;34m"         # Blue
    Purple="\033[0;35m"       # Purple
    Cyan="\033[0;36m"         # Cyan
    White="\033[0;37m"        # White
    NoCo="\033[0:0m"

class GoogleAnalysis(object):
    """docstring for GoogleAnalysis."""
    def __init__(self):
        super(GoogleAnalysis, self).__init__()
        self.api = GooglePlayAPI(ANDROID_ID)
        self.api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

    def category_list(self):
        response = self.api.browse()
        return list(map(lambda c: SEPARATOR.join(i.encode('utf8') for i in [urlparse.parse_qs(c.dataUrl)['browse?cat'][0]]), response.category))

    def read_files(self, cate):
        with open(dirname(__file__) + '/resource_list/' + cate + '.txt', 'r') as f:
            for line in f.readlines():
                filename = line.strip()
                print Color.Green + '[!] Start:  ' + Color.NoCo +filename
                self.details(filename)

    def details(self, packageName):
        message = self.api.details(packageName).docV2
        result = {
            "docid": message.docid,
            "title": message.title,
            "creator": message.creator,
            "descriptionHtml": message.descriptionHtml,
            "offer": {
                "currencyCode": message.offer[0].currencyCode,
                "formattedAmount": message.offer[0].formattedAmount
            },
            "details": {
                "appDetails": {
                    "developerName": message.details.appDetails.developerName,
                    "versionCode": message.details.appDetails.versionCode,
                    "versionString": message.details.appDetails.versionString,
                    "contentRating": message.details.appDetails.contentRating,
                    "installationSize": message.details.appDetails.installationSize,
                    # "permission": message.details.appDetails.permission,
                    "numDownloads": message.details.appDetails.numDownloads,
                    "packageName": message.details.appDetails.packageName,
                    "uploadDate": message.details.appDetails.uploadDate,
                }
            },
            "aggregateRating": {
              "starRating": message.aggregateRating.starRating,
              "ratingsCount": message.aggregateRating.ratingsCount,
              "oneStarRatings": message.aggregateRating.oneStarRatings,
              "twoStarRatings": message.aggregateRating.twoStarRatings,
              "threeStarRatings": message.aggregateRating.threeStarRatings,
              "fourStarRatings": message.aggregateRating.fourStarRatings,
              "fiveStarRatings": message.aggregateRating.fiveStarRatings,
              "commentCount": message.aggregateRating.commentCount
            }
        }

        doc = message
        vc = doc.details.appDetails.versionCode
        ot = doc.offer[0].offerType
        self.download(packageName, vc, ot)


        with open(dirname(abspath(__file__)) + '/detail_reports/' + packageName, 'w') as f:
            json.dump(result, f, sort_keys=True, indent=4, separators=(',', ': '))
            f.close()
        # print json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

    def download(self, packageName, vc, ot):
        data = self.api.download(packageName, vc, ot)

        with open(dirname(abspath(__file__)) + '/apk_files/' + packageName + '.apk', 'w') as f:
            f.write(data)
            print "Done"
            f.close()

    def test(self):
        lists = list('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c')
        for i in lists:
            try:
                print self.api.list('ART_AND_DESIGN', 'apps_topselling_free', '1', 'CA'+i)
            except:
                print i

def main():
    analysis = GoogleAnalysis()
    packageName = 'com.UsedClothCraftIdeas.BabidiArt'
    analysis.read_files('ART_AND_DESIGN')
    # analysis.details(packageName)
    # analysis.show_detail()


if __name__ == '__main__':
    main()
