# SSRFinder

## An *assistant* to help you find SSRF vulns

### Usage:

`Usage: python SSRFinder.py <DOMAIN> <OPTIONS>`

### What is this tool?

This is a tool which will:
- Crawl through a given domain
- Collect URLs from `<a>` tags 
- Continue to crawl through these untill either all URLs are found **OR** you give a KeyboardInterrupt (Ctrl + C)
- Then sort through the found URLS to find URLS with other URLs in the get parameter
- Prints them for you to further investigate in order to potentially find SSRFs

### Contact me

If you want to report bugs, offer suggestions etc, contact me at Contact@Josephwitten.com

### Misc Notes

- The vauger your input, eg "google.com" the longer it will take/more likely to run into bugs
- for best results give specific sub domains
- Only find GET request based SSRF, **not post**

### To add in the future:

- Automated fuzzer for common SSRF payloads?
- Rate limiting of get requests

### Obvious legal comments

- Only use this against authorized domain
- Check the scope for use of automated tools
