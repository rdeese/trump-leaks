from lxml import html
import requests
from unidecode import unidecode

blog_urls = [
  "https://civisanalytics.com/blog/data-science/2016/10/25/assessing-data-item-response-theory/",
  "https://civisanalytics.com/blog/data-science/2016/10/18/pydata-chicago/",
  "https://civisanalytics.com/blog/news-and-insights/2016/10/12/momentum-rising-star-award/",
  "https://civisanalytics.com/blog/data-science/2016/10/04/who-won-the-debate/",
  "https://civisanalytics.com/blog/data-science/2016/09/22/neural-network-visualization/",
  "https://civisanalytics.com/blog/data-science/2016/09/15/cancer-moonshot-people-and-skills/",
  "https://civisanalytics.com/blog/data-science/2016/09/13/cancer-moonshot-data-sharing/",
  "https://civisanalytics.com/blog/data-science/2016/09/09/cancer-moonshot-data-infrastructure/",
  "https://civisanalytics.com/blog/data-science/2016/08/31/gephi-force-diagram-tool/",
  "https://civisanalytics.com/blog/data-science/2016/08/25/glmnet-python/",
  "https://civisanalytics.com/blog/data-science/2016/08/15/python-r/",
  "https://civisanalytics.com/blog/life-at-civis/2016/08/09/design-sprint-researchers-perspective/",
  "https://civisanalytics.com/blog/tech/2016/07/26/building-design-culture/",
  "https://civisanalytics.com/blog/data-science/2016/07/20/customer-acquisition-survey-modeling/",
  "https://civisanalytics.com/blog/life-at-civis/2016/06/29/policies-support-work-life-balance/",
  "https://civisanalytics.com/blog/engineering/2016/06/14/using-sumo-logic-for-authentication-auditing/",
  "https://civisanalytics.com/blog/news-and-insights/2016/06/07/web-surveys-designed-by-you-powered-by-data-science/",
  "https://civisanalytics.com/blog/news-and-insights/2016/06/02/unexpected-insights-from-repurposed-data/",
  "https://civisanalytics.com/blog/life-at-civis/2016/05/24/people-behind-people-science-work-life-balance/",
  "https://civisanalytics.com/blog/data-science/2016/05/11/strata-2016-talk/",
  "https://civisanalytics.com/blog/data-science/2016/05/03/it-was-always-trump/",
  "https://civisanalytics.com/blog/news-and-insights/2016/05/03/before-you-ask-america-anything-ask-right-questions/",
  "https://civisanalytics.com/blog/data-science/2016/04/20/bringing-data-science-to-government/",
  "https://civisanalytics.com/blog/data-science/2016/04/14/ask-america-anything-results/",
  "https://civisanalytics.com/blog/news-and-insights/2016/03/30/q-and-a-with-usa-for-unhcr-on-using-data/",
  "https://civisanalytics.com/blog/news-and-insights/2016/03/08/Grace-Hopper-Impact-Report/",
  "https://civisanalytics.com/blog/engineering/2016/02/29/2016-endless-hackweek/",
  "https://civisanalytics.com/blog/data-science/2016/02/25/analysis-of-republican-twitter-follower-interests/",
  "https://civisanalytics.com/blog/data-science/2016/02/18/viewing-presidential-primary-through-twitter/",
  "https://civisanalytics.com/blog/news-and-insights/2016/02/11/using-data-science-to-message-test-super-bowl-ads/",
  "https://civisanalytics.com/blog/engineering/2016/02/05/open-source-at-civis-analytics/",
  "https://civisanalytics.com/blog/engineering/2016/02/04/rubyaudit-tirelessly-auditing-ruby-and-rubygem/",
  "https://civisanalytics.com/blog/life-at-civis/2016/01/26/data-scientist-tops-glassdoor-best-jobs-list/",
  "https://civisanalytics.com/blog/news-and-insights/2016/01/21/q-and-a-with-discovery-on-civis-media-optimizer/",
  "https://civisanalytics.com/blog/data-science/2016/01/15/data-science-on-state-of-the-union-addresses/",
  "https://civisanalytics.com/blog/data-science/2016/01/13/connect-the-civis-platform-to-google-sheets/",
  "https://civisanalytics.com/blog/data-science/2016/01/06/workflows-python-using-pipeline-gridsearchcv-for-compact-code/",
  "https://civisanalytics.com/blog/data-science/2015/12/31/republican-primary-in-one-gif/",
  "https://civisanalytics.com/blog/data-science/2015/12/23/workflows-in-python-curating-features-and-thinking-scientifically-about-algorithms/",
  "https://civisanalytics.com/blog/data-science/2015/12/17/workflows-in-python-getting-data-ready-to-build-models/",
  "https://civisanalytics.com/blog/data-science/2015/12/09/data-storytelling-and-feature-creation/",
  "https://civisanalytics.com/blog/data-science/2015/12/04/exploring-virtual-reality-data-visualization-with-the-gear-vr/",
  "https://civisanalytics.com/blog/data-science/2015/12/01/ask-america-anything/",
  "https://civisanalytics.com/blog/life-at-civis/2015/11/17/lightning-talks-at-Civis-Analytics/",
  "https://civisanalytics.com/blog/life-at-civis/2015/11/10/civis-analytics-and-the-practical-innovator/",
  "https://civisanalytics.com/blog/engineering/2015/10/28/on-the-technical-google-hangout/",
  "https://civisanalytics.com/blog/data-science/2015/10/21/best-practices-for-nonprofit-leaders/",
  "https://civisanalytics.com/blog/life-at-civis/2015/10/14/finding-your-fellow-weirdos/",
  "https://civisanalytics.com/blog/news-and-insights/2015/10/07/our-open-letter-to-madison-ave-in-NYT/",
"https://civisanalytics.com/blog/news-and-insights/2015/10/06/dear-madison-ave-dont-quit-tv/",
"https://civisanalytics.com/blog/engineering/2015/10/02/using-swagger-to-detect-breaking-api-changes/",
"https://civisanalytics.com/blog/engineering/2015/09/18/guiding-summer-interns-to-become-effective-engineers/",
"https://civisanalytics.com/blog/engineering/2015/09/10/Adventures-in-MySQL-When-Composite-Indexes-Go-Long/",
"https://civisanalytics.com/blog/data-science/2015/09/02/civis-api-scale-up-your-data-science/",
"https://civisanalytics.com/blog/data-science/2015/08/26/republican-primary-poll-august2015/",
"https://civisanalytics.com/blog/data-science/2015/08/13/scipy-2015-building-predictive-modeling-with-python/",
"https://civisanalytics.com/blog/data-science/2015/08/06/meet-civis-favorite-features-of-data-science-platform/",
"https://civisanalytics.com/blog/engineering/2015/07/29/elegant-aws-access-management-iam-role-injector/",
"https://civisanalytics.com/blog/data-science/2015/07/21/data-science-pop-up-chicago/",
"https://civisanalytics.com/blog/news-and-insights/2015/06/30/Bigger-Cheaper-Faster-Data-in-the-Cloud/",
"https://civisanalytics.com/blog/data-science/2015/06/29/SCOTUS-the-ACA-and-Twitter/",
"https://civisanalytics.com/blog/data-science/2015/04/15/strata-2015-talk/",
"https://civisanalytics.com/blog/news-and-insights/2015/04/09/Civis-Analytics-and-AWS/",
"https://civisanalytics.com/blog/news-and-insights/2015/02/25/partnering-with-discovery/",
"https://civisanalytics.com/blog/life-at-civis/2014/12/22/civis-or-the-academy/",
"https://civisanalytics.com/blog/news-and-insights/2014/12/22/building-stuff-at-aws-re-invent/",
"https://civisanalytics.com/blog/data-science/2014/11/02/the-medicaid-counterfactual-how-we-ran-the-simulation/",
"https://civisanalytics.com/blog/news-and-insights/2014/10/29/a-formula-to-find-the-uninsured/",
"https://civisanalytics.com/blog/news-and-insights/2014/10/29/obamacare-who-was-helped-the-most/",
"https://civisanalytics.com/blog/data-science/2014/10/28/cmu-recruiting-recap/",
"https://civisanalytics.com/blog/news-and-insights/2014/10/22/city-uses-new-technology-to-target-women-encourage-mammography/",
"https://civisanalytics.com/blog/news-and-insights/2014/10/02/7-fast-growing-Chicago-tech-companies-that-are-hiring-right-now/",
"https://civisanalytics.com/blog/data-science/2014/08/25/a-menagerie-of-tattoos/",
"https://civisanalytics.com/blog/data-science/2014/08/20/why-we-love-models/",
"https://civisanalytics.com/blog/life-at-civis/2014/08/15/summer-interns-and-fellows/",
"https://civisanalytics.com/blog/data-science/2014/08/14/piaggio-case-study/",
"https://civisanalytics.com/blog/engineering/2014/08/14/Using-Docker-to-Run-Python/",
"https://civisanalytics.com/blog/data-science/2014/08/13/measuring-pi-with-lentils-and-python/",
"https://civisanalytics.com/blog/engineering/2014/08/12/person-matching-on-aws/",
"https://civisanalytics.com/blog/data-science/2014/08/04/How-Forecasting-Revolutionized-Election-Resource-Allocation/",
"https://civisanalytics.com/blog/life-at-civis/2014/07/18/interview-tips/",
"https://civisanalytics.com/blog/news-and-insights/2014/06/19/civis-wins-the-moxie-awards-best-new-startup/",
"https://civisanalytics.com/blog/life-at-civis/2014/06/01/anniversary-science-fair/",
"https://civisanalytics.com/blog/news-and-insights/2014/05/30/obamas-data-gurus-find-life-outside-the-beltway/",
"https://civisanalytics.com/blog/news-and-insights/2014/05/30/ex-obama-techies-celebrate-birthday-with-science-fair/",
"https://civisanalytics.com/blog/news-and-insights/2014/04/24/5-chicago-ctos-gabriel-burt/",
"https://civisanalytics.com/blog/news-and-insights/2012/12/19/how-president-obamas-campaign-used-big-data/"
]

corpus = open('civis-corpus.txt', 'w')

print len(blog_urls)
i = 0
for url in blog_urls:
  i += 1
  print i
  page = requests.get(url)
  tree = html.fromstring(page.content)

  content = tree.xpath('//article[@class="post-content"]/p/text()')

  # Clean content
  content = '\n'.join(content)
  content = unidecode(content)

  corpus.write(content)

corpus.close()
