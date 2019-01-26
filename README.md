[![Build Status](https://travis-ci.com/danquack/Sitemap-Prerendering-S3.svg?branch=master)](https://travis-ci.com/danquack/Sitemap-Prerendering-S3)
[![Code Coverage](https://codecov.io/gh/danquack/Sitemap-Prerendering-S3/branch/master/graph/badge.svg)](https://codecov.io/gh/danquack/Sitemap-Prerendering-S3)

# Sitemap Prerendering
This module was designed to run as a prerender client that caches to s3. Utilizing either local or docker to render webpages, which are then posts the rendered static HTML page to S3. The idea behind this is to allow for a place for bots to scan static html pages.

## Prereqs
- Create an S3 Bucket. 
- Have a domain with a robots.txt (ex. https://example.com/robots.txt)

## Utilization
### Docker
<code>
 docker build -t sitemap-prerender . 
 docker run -e AWS_ACCESS_KEY_ID=AWSKEY -e AWS_SECRET_ACCESS_KEY=AWSSECRET -t sitemap-prerender -i python -c "from prerender.prerender import Prerender; Prerender(#Options).capture()"
</code>

### Development

If developing, ensure to install the requirements.txt file.

<code>pip install -r requirements.txt</code>

### Module Installation
Install the modules:

<code>
python scraper/setup.py install
python prerender/setup.py install
</code>

<br>

Then from within your python code:

<code>
from prerender.prerender import Prerender

pre = Prerender(
    # Options
)</code>

To invalidate bucket:

<code>
pre.invalidate()
</code>

To capture pages into s3 bucket:

<code>
pre.capture()
</code>


#### Options
<table>
  <thead>
    <th>
      Required
    </th>
    <th>
      Variable
    </th>
    <th>
      Info
    </th>
  </thead>
  <tr>
    <td>
      True
    </td>
    <td>
      robots_url
    </td>
    <td>
      The path to your root robots file. This will contain the sitemap info
    </td>
  </tr>
  <tr>
    <td>
      True
    </td>
    <td>
      s3_bucket
    </td>
    <td>
      Cache Archive bucket name
    </td>
  </tr>
    <tr>
    <td>
      False
    </td>
    <td>
      auth
    </td>
    <td>
      Utilized for basic authenticating to page.
    </td>
  </tr>
    </tr>
    <tr>
    <td>
      False
    </td>
    <td>
      query_char_deliminator
    </td>
    <td>
      (recommended) - Character to replace the question mark. 
      If storing static pages, AWS doesnt allow you to have ? in a file to serve the content. So changing to a different character will fix this.
      Ex) /subpage?id=1 and your query_char_deliminator is '#', your page will be stored as /subpage#id=1
    </td>
  </tr>
  <tr>
    <td>
      False
    </td>
    <td>
      allowed_domains
    </td>
    <td>
      List of domains to allow. If specified all other domains will be blocked during the page capturing.
    </td>
  </tr>
</table>