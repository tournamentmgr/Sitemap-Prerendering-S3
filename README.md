[![Build Status](https://travis-ci.com/danquack/Sitemap-Prerendering-S3.svg?branch=master)](https://travis-ci.com/danquack/Sitemap-Prerendering-S3)
[![Code Coverage](https://codecov.io/gh/danquack/Sitemap-Prerendering-S3/branch/master/graph/badge.svg)](https://codecov.io/gh/danquack/Sitemap-Prerendering-S3)

# Sitemap Prerendering
This module was designed to run as a prerender client that caches to s3. Utilizing either local or docker to render webpages, which are then posts the rendered static HTML page to S3. The idea behind this is to allow for a place for bots to scan static html pages. A .html extension is added to every page.

## Prereqs
- Create an S3 Bucket. 
- Have a domain with a sitemap (ex. https://google.com/sitemap.xml)

## Utilization
### Docker
<code>
 docker build -t sitemap-prerender . 
 docker run -e AWS_ACCESS_KEY_ID=AWSKEY -e AWS_SECRET_ACCESS_KEY=AWSSECRET -t sitemap-prerender -i python -c "from prerender.prerender import Prerender; Prerender(#Options).capture()"
</code>

### Local
Install the modules:

<code>python setup.py install</code>

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
      site_map_url
    </td>
    <td>
      The path to your root sitemap,
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
      check_valid
    </td>
    <td>
      Checks rather the provided site map url exists for the root sitemap
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
</table>