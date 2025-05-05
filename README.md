# nginx configurations

This repo contains my Nginx configuration files for blocking scraping bots on various websites I manage. Since November 2024, I've observed a fat spike in requests, predominantly from IP ranges from a few cloud providers. The configuration files in this repository help block those specific IP ranges.

I've been using and manually curating these since January 2023.

Feel free to copy-paste and protect your own server.

## files
There are two main configuration files:

- **blocked_ip**: List of addresses that are **disallowed** to be served requests. In production I typically `return 444` to these.
- **blocked_ua**: List of user agents that are **disallowed** from accessing the site.

I maintain an additional config file for IP addresses that are not necessarily "bad" crawlers, These IP addresses are generally rate limited or are only disallowed on expensive dynamic pages such as MediaWiki's search, auto-generated git pages, diffs, etc. I generally don't upload this file to my servers.

- **restricted_ip**: List of addresses that can access static pages, but receive `return 403` or rate-limit on dynamic pages

I aim to support "good bots", so well-known crawlers like Googlebot, Bing or yandex are not blocked, although they may be restricted.

## reasoning
Over the past few months, I've spent a good deal of time in any given week dealing with these fucking LLM crawlers. While decent bots like Googlebot respect `/robots.txt` and crawl maybe a few times a minute, the recent surge of LLM/GenAI crawlers has saturated the compute available in my servers, significantly slowing down load times and worsening the user experience for everyone involved. Last week, one of my Git servers went offline because they repeatedly kept hitting expensive endpoints. As a result, I've decided to just block their IP ranges, as I have no need for them.

Additionally, I've seen various of these weird SEO-optimizing services over the years that I'm never going to purchase, so I've opted to block them too (ahrefs? siteaudit? mojave12? seznam? i don't care??)

## how to use
Dump the generated `blocked_xxx.conf` file into your `/etc/nginx/conf.d/`. You can then modify your `server` and `location` blocks depending on whether you want to block a bot:

```
server {
	listen 80;
	// ...

	if ($blocked_ip) {
		return 403;
	}

	location / {
		try_files ...
	}
```

I'm aware about `ìf` being discouraged and evil, but in this case the variables are being set in a `map` outside of the server and not used in a location block.

## sources

Most of these come from analying offending IP addresses manually in `ipinfo.io` and blocking their entire CIDR range.

Since January 2023, I have enabled access logs and been actively managing bot traffic.

## other solutions

- [Anubis](https://anubis.techaro.lol/)
- [go-away](https://git.gammaspectra.live/git/go-away)
- Cloudflare's MITM captcha
