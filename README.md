[![Actions Status](https://github.com/tournamentmgr/Sitemap-Prerendering-S3/workflows/test/badge.svg)](https://github.com/mattcat10/tournamentmgr-api/actions)
[![Code Coverage](https://codecov.io/gh/tournamentmgr/Sitemap-Prerendering-S3/branch/master/graph/badge.svg)](https://codecov.io/gh/danquack/Sitemap-Prerendering-S3)

# Sitemap Prerendering
This module was designed to run as a prerender client that caches to s3. Utilizing either local or docker to render webpages, which are then posts the rendered static HTML page to S3. The idea behind this is to allow for a place for bots to scan static html pages.

## Prereqs
- Create an S3 Bucket. 
- Have a domain with a robots.txt (ex. https://example.com/robots.txt)

## Development

If developing, ensure to install the requirements.txt file.

<code>pip install -r requirements.txt</code>


## Utilization
### Docker
<code>
 docker build -t prerender .
 
 docker run -e AWS_ACCESS_KEY_ID=AWSKEY -e AWS_SECRET_ACCESS_KEY=AWSSECRET -t prerender -i python -c "from prerender.prerender import Prerender; Prerender(#Options).capture()"
</code>

### Local Installation
#### Install the modules:

<code>
python scraper/setup.py install

python prerender/setup.py install
</code>

<br>

#### Create Python Code
<code>
from prerender.prerender import Prerender

pre = Prerender(
    # Options
)</code>


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



## Module invocation
#### Invalidate/Clear bucket:

<code>
pre.invalidate()
</code>

#### Capture from sitemaps within Robots.txt

<code>
pre.capture()
</code>

#### Single Page Capture
If you prefer to capture a single page, versus a full domain.

<code>
pre.capture_page_and_upload("https://example.com")
</code>

